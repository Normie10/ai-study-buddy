"""Secțiune: Completează spațiul liber.

O propoziție cu un cuvânt lipsă, marcat cu _____ : scrii răspunsul și vezi
imediat dacă ai nimerit, cu explicație și sursă. La final primești scorul.

Comparare TOLERANTĂ: fără diacritice, fără majuscule, și acceptă mici greșeli
de scriere (câteva litere diferite, în funcție de lungimea cuvântului). De
asemenea acceptă mai multe formulări corecte pentru același răspuns, date de
AI o singură dată la generare, ca să nu facem o cerere nouă la Google la
fiecare verificare.
"""

import json
import unicodedata
from collections import Counter

import streamlit as st

from generare import cere_model
from memorie import preia_din_teanc
from utile import eticheta_grup, text_din_unitati

NUME = "Completează"
ORDINE = 27  # poziția în listă: numerele mici apar primele
CERE_MATERIAL = True
DESCRIERE = (
    "Propoziții din materialul tău, cu un cuvânt lipsă. Scrii răspunsul și vezi "
    "imediat dacă ai nimerit, cu explicație și sursa din document."
)

CHEIE = "comp_sesiune"
DIM_TEANC_COMPLETARE = 30  # cât cerem la Google dintr-o dată


def _norm_comp(text):
    """Litere mici + elimină diacriticele (ă, â, î, ș, ț), pentru comparare
    tolerantă la diacritice și majuscule."""
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def _distanta(a, b):
    """Distanța Levenshtein (câte litere trebuie schimbate/adăugate/șterse ca
    să transformi a în b)."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    anterior = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curent = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curent[j] = min(
                anterior[j] + 1,  # ștergere
                curent[j - 1] + 1,  # inserare
                anterior[j - 1] + cost,  # înlocuire
            )
        anterior = curent
    return anterior[-1]


def _toleranta(cuvant):
    """Câte litere diferite acceptăm, în funcție de lungime."""
    n = len(cuvant)
    if n <= 4:
        return 0
    if n <= 7:
        return 1
    return 2


def _e_apropiat(raspuns_dat, raspuns_bun):
    """True dacă răspunsul dat e identic sau suficient de apropiat de cel bun."""
    a = _norm_comp(raspuns_dat)
    b = _norm_comp(raspuns_bun)
    if a == b:
        return True
    if not a:
        return False
    return _distanta(a, b) <= _toleranta(b)


# ------------------------- generare (din document) -------------------------
def _parse_json(text):
    curat = text.replace("```json", "").replace("```", "").strip()
    return json.loads(curat)


def _valideaza_completare(lista, unitate):
    bune = []
    for e in lista:
        try:
            intrebare = str(e["intrebare"]).strip()
            raspuns = str(e["raspuns"]).strip()
            if not intrebare or not raspuns or "_____" not in intrebare:
                continue
            variante = [str(v).strip() for v in e.get("variante_acceptate", []) if str(v).strip()]
            bune.append(
                {
                    "intrebare": intrebare,
                    "raspuns": raspuns,
                    "variante_acceptate": variante,
                    "pagina": e.get("pagina", "?"),
                    "unitate": unitate,
                    "explicatie": str(e.get("explicatie", "")),
                }
            )
        except Exception:
            continue
    if not bune:
        raise ValueError("Niciun element valid în răspuns")
    return bune


def genereaza_teanc_completare(client, unitati, eticheta, dificultate, limba):
    prompt = f"""Ești un profesor care creează exerciții de completat spațiul liber.
Pe baza TEXTULUI de mai jos, creează cât mai multe propoziții distincte, dar
maximum {DIM_TEANC_COMPLETARE}, dificultate {dificultate}, în limba {limba}.

Reguli:
- Folosește DOAR informații din text.
- Fiecare propoziție are UN SINGUR cuvânt sau o sintagmă scurtă lipsă (nu o
  frază lungă), marcată exact cu _____ (cinci underscore) în locul ei.
- Alege cuvinte sau termeni importanți (nu cuvinte banale de legătură).
- "raspuns" este cuvântul/sintagma exactă care lipsește.
- "variante_acceptate" este o listă (poate fi goală) cu alte formulări corecte
  ale aceluiași răspuns (de exemplu singular/plural dacă ambele sunt corecte
  gramatical, sau o prescurtare uzuală). NU repeta "raspuns" în această listă.
- Fiecare propoziție tratează un alt aspect; nu repeta și nu reformula.
- În "explicatie" spune pe scurt de ce acesta e răspunsul corect.
- În câmpul "pagina" pune numărul din eticheta [{eticheta.capitalize()} N] a
  fragmentului de unde provine informația.
- Răspunde DOAR cu JSON valid, fără alt text, în formatul:
[{{"intrebare": "... _____ ...", "raspuns": "...", "variante_acceptate": ["..."], "pagina": 1, "explicatie": "..."}}]

TEXT:
{text_din_unitati(unitati, eticheta)}"""
    return cere_model(
        client, prompt, lambda t: _valideaza_completare(_parse_json(t), eticheta)
    )


# ------------------------- interfață -------------------------
def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _porneste(intrebari, info, hash_material):
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "intrebari": intrebari,
        "info": info,
        "idx": 0,
        "raspunsuri": {},  # poziția -> (text_dat, e_corect, aproape)
    }


def _verifica(idx, raspuns_dat, q):
    s = st.session_state.get(CHEIE)
    if not s or idx in s["raspunsuri"]:
        return
    toate_bune = [q["raspuns"]] + list(q.get("variante_acceptate", []))
    e_corect = any(_e_apropiat(raspuns_dat, bun) for bun in toate_bune)
    e_exact = _norm_comp(raspuns_dat) in {_norm_comp(b) for b in toate_bune}
    aproape = e_corect and not e_exact
    s["raspunsuri"][idx] = (raspuns_dat, e_corect, aproape)


def _urmatoarea():
    s = st.session_state.get(CHEIE)
    if s:
        s["idx"] += 1


def _inceput_nou():
    st.session_state.pop(CHEIE, None)


def _repeta_gresite():
    s = st.session_state.get(CHEIE)
    if not s:
        return
    gresite = [
        q for i, q in enumerate(s["intrebari"])
        if not s["raspunsuri"].get(i, (None, False, False))[1]
    ]
    if gresite:
        _porneste(gresite, s["info"], s["hash"])


def _setari(ctx):
    c1, c2 = st.columns(2)
    nr = c1.number_input("Număr întrebări", 3, 30, 10, key="comp_nr")
    dif = c2.selectbox(
        "Dificultate", ["ușoară", "medie", "grea"], index=1, key="comp_dif"
    )

    if st.button("Începe", key="comp_start"):
        with st.spinner("Pregătesc întrebările..."):
            try:
                elemente, model, nota = preia_din_teanc(
                    ("comp", ctx.hash_material, dif, ctx.limba),
                    nr,
                    "intrebare",
                    lambda: genereaza_teanc_completare(
                        ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
                    ),
                )
            except Exception as e_comp:
                st.error(f"A apărut o eroare: {e_comp}")
                return
        if not elemente:
            st.error("Nu am găsit întrebări potrivite în acest material.")
            return
        info = f"{model} · {nota}"
        if len(elemente) < nr:
            info += f" (am găsit doar {len(elemente)} întrebări distincte)"
        _porneste(elemente, info, ctx.hash_material)
        st.rerun()


def _intrebare(s):
    total = len(s["intrebari"])
    i = s["idx"]
    q = s["intrebari"][i]
    stare = s["raspunsuri"].get(i)
    corecte = sum(1 for v in s["raspunsuri"].values() if v[1])

    st.progress(i / total, text=f"Întrebarea {i + 1} din {total}")
    st.caption(f"Model: {s['info']}")

    with st.container(border=True):
        st.markdown("**Completează spațiul liber:**")
        st.subheader(_md(q["intrebare"]))

    if stare is None:
        raspuns_dat = st.text_input("Răspunsul tău", key=f"comp_text_{i}")
        if st.button("Verifică", key=f"comp_verifica_{i}", type="primary"):
            _verifica(i, raspuns_dat, q)
            st.rerun()
    else:
        text_dat, e_corect, aproape = stare
        if e_corect and not aproape:
            st.success(f"Corect! Ai scris: „{text_dat}”.")
        elif e_corect and aproape:
            st.success(
                f"Corect (ai greșit puțin scrierea). Ai scris: „{text_dat}”, "
                f"forma corectă e „{q['raspuns']}”."
            )
        else:
            st.error(f"Greșit. Ai scris: „{text_dat}”. Răspunsul corect: {q['raspuns']}.")
        if q.get("explicatie"):
            st.markdown(_md(q["explicatie"]))
        st.caption(f"{q.get('unitate', 'pagina').capitalize()} {q.get('pagina', '?')}")
        ultima = i + 1 >= total
        st.button(
            "Vezi rezultatul" if ultima else "Următoarea",
            on_click=_urmatoarea,
            key="comp_next",
            use_container_width=True,
            type="primary",
        )
    st.caption(f"Corecte până acum: {corecte} din {len(s['raspunsuri'])}")


def _rezultate(s):
    total = len(s["intrebari"])
    gresite = [
        (i, q) for i, q in enumerate(s["intrebari"])
        if not s["raspunsuri"].get(i, (None, False, False))[1]
    ]
    scor = total - len(gresite)
    procent = round(100 * scor / total)

    st.progress(1.0, text="Ai terminat")
    c1, c2 = st.columns(2)
    c1.metric("Scor", f"{scor}/{total}")
    c2.metric("Procent", f"{procent}%")

    if not gresite:
        st.success("Ai răspuns corect la toate întrebările. Bravo!")
    else:
        st.subheader("Ce să recapitulezi")
        grupuri = Counter(eticheta_grup(q) for _, q in gresite)
        for eticheta, nr in grupuri.most_common():
            cuvant = "întrebare greșită" if nr == 1 else "întrebări greșite"
            st.markdown(f"- **{eticheta}**: {nr} {cuvant}")
        st.caption(
            "Locurile indicate sunt cele date de model pentru fiecare întrebare. "
            "Verifică-le în document."
        )
        with st.expander("Vezi întrebările greșite"):
            for i, q in gresite:
                text_dat = s["raspunsuri"].get(i, ("(fără răspuns)", False, False))[0]
                st.markdown(f"**{i + 1}. {_md(q['intrebare'])}**")
                st.markdown(
                    f"Răspunsul tău: {text_dat or '(fără răspuns)'}. "
                    f"Răspuns corect: {q['raspuns']}."
                )
                if q.get("explicatie"):
                    st.caption(_md(q["explicatie"]))
                st.divider()

    b1, b2 = st.columns(2)
    if gresite:
        b1.button(
            "Repetă doar întrebările greșite",
            on_click=_repeta_gresite,
            key="comp_repeta",
            use_container_width=True,
        )
    b2.button(
        "Început nou",
        on_click=_inceput_nou,
        key="comp_nou",
        use_container_width=True,
    )


def afiseaza(ctx):
    """Funcția pe care o apelează aplicația pentru această secțiune."""
    st.caption(DESCRIERE)

    s = st.session_state.get(CHEIE)
    if s and s["hash"] != ctx.hash_material:
        st.session_state.pop(CHEIE, None)  # s-a schimbat materialul
        s = None

    if s is None:
        _setari(ctx)
    elif s["idx"] < len(s["intrebari"]):
        _intrebare(s)
    else:
        _rezultate(s)
