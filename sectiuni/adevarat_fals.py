"""Secțiune: Adevărat / Fals.

O afirmație pe rând: răspunzi cu Adevărat sau Fals și vezi imediat dacă ai
nimerit, cu explicație și sursă. La final primești scorul și ce să recapitulezi.

Așa arată orice secțiune nouă: un fișier în folderul sectiuni/ cu cele patru
setări de mai jos și o funcție afiseaza(ctx). Aplicația o găsește singură.
"""

from collections import Counter

import streamlit as st

from export_html import html_quiz
from generare import genereaza_teanc_af
from memorie import preia_din_teanc
from utile import eticheta_grup

NUME = "Adevărat / Fals"
ORDINE = 25  # poziția în listă: numerele mici apar primele
CERE_MATERIAL = True  # False = merge și fără document (ca SAT)
DESCRIERE = (
    "Afirmații din materialul tău. Răspunzi pe rând cu Adevărat sau Fals și vezi "
    "imediat dacă ai nimerit, cu explicație și sursa din document."
)

CHEIE = "afs_sesiune"  # unde ținem în memorie sesiunea curentă


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _porneste(intrebari, info, hash_material):
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "intrebari": intrebari,
        "info": info,
        "idx": 0,
        "raspunsuri": {},  # poziția afirmației -> 0 (Adevărat) sau 1 (Fals)
    }


def _raspunde(alegere):
    s = st.session_state.get(CHEIE)
    if s and s["idx"] not in s["raspunsuri"]:
        s["raspunsuri"][s["idx"]] = alegere


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
        q for i, q in enumerate(s["intrebari"]) if s["raspunsuri"].get(i) != q["corect"]
    ]
    if gresite:
        _porneste(gresite, s["info"], s["hash"])


def _setari(ctx):
    c1, c2 = st.columns(2)
    nr = c1.number_input("Număr afirmații", 3, 30, 10, key="afs_nr")
    dif = c2.selectbox(
        "Dificultate", ["ușoară", "medie", "grea"], index=1, key="afs_dif"
    )

    if st.button("Începe", key="afs_start"):
        with st.spinner("Pregătesc afirmațiile..."):
            try:
                elemente, model, nota = preia_din_teanc(
                    ("af", ctx.hash_material, dif, ctx.limba),
                    nr,
                    "intrebare",
                    lambda: genereaza_teanc_af(
                        ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
                    ),
                )
            except Exception as e_af:
                st.error(f"A apărut o eroare: {e_af}")
                return
        if not elemente:
            st.error("Nu am găsit afirmații în acest material.")
            return
        info = f"{model} · {nota}"
        if len(elemente) < nr:
            info += f" (am găsit doar {len(elemente)} afirmații distincte)"
        _porneste(elemente, info, ctx.hash_material)
        st.rerun()


def _intrebare(s):
    total = len(s["intrebari"])
    i = s["idx"]
    q = s["intrebari"][i]
    raspuns = s["raspunsuri"].get(i)
    corecte = sum(
        1 for j, a in s["raspunsuri"].items() if a == s["intrebari"][j]["corect"]
    )

    st.progress(i / total, text=f"Afirmația {i + 1} din {total}")
    st.caption(f"Model: {s['info']}")

    with st.container(border=True):
        st.markdown("**Adevărat sau fals?**")
        st.subheader(_md(q["intrebare"]))

    if raspuns is None:
        b1, b2 = st.columns(2)
        b1.button(
            "Adevărat",
            on_click=_raspunde,
            args=(0,),
            key="afs_adev",
            use_container_width=True,
        )
        b2.button(
            "Fals",
            on_click=_raspunde,
            args=(1,),
            key="afs_fals",
            use_container_width=True,
        )
    else:
        if raspuns == q["corect"]:
            st.success("Corect!")
        else:
            st.error(f"Greșit. Răspunsul corect: {q['variante'][q['corect']]}.")
        if q.get("explicatie"):
            st.markdown(_md(q["explicatie"]))
        st.caption(f"{q.get('unitate', 'pagina').capitalize()} {q.get('pagina', '?')}")
        ultima = i + 1 >= total
        st.button(
            "Vezi rezultatul" if ultima else "Următoarea",
            on_click=_urmatoarea,
            key="afs_next",
            use_container_width=True,
            type="primary",
        )
    st.caption(f"Corecte până acum: {corecte} din {len(s['raspunsuri'])}")


def _rezultate(s):
    total = len(s["intrebari"])
    gresite = [
        (i, q)
        for i, q in enumerate(s["intrebari"])
        if s["raspunsuri"].get(i) != q["corect"]
    ]
    scor = total - len(gresite)
    procent = round(100 * scor / total)

    st.progress(1.0, text="Ai terminat")
    c1, c2 = st.columns(2)
    c1.metric("Scor", f"{scor}/{total}")
    c2.metric("Procent", f"{procent}%")

    if not gresite:
        st.success("Ai răspuns corect la toate afirmațiile. Bravo!")
    else:
        st.subheader("Ce să recapitulezi")
        grupuri = Counter(eticheta_grup(q) for _, q in gresite)
        for eticheta, nr in grupuri.most_common():
            cuvant = "afirmație greșită" if nr == 1 else "afirmații greșite"
            st.markdown(f"- **{eticheta}**: {nr} {cuvant}")
        st.caption(
            "Locurile indicate sunt cele date de model pentru fiecare afirmație. "
            "Verifică-le în document."
        )
        with st.expander("Vezi afirmațiile greșite"):
            for i, q in gresite:
                ales = s["raspunsuri"].get(i)
                ales_text = q["variante"][ales] if ales is not None else "fără răspuns"
                st.markdown(f"**{i + 1}. {_md(q['intrebare'])}**")
                st.markdown(
                    f"Răspunsul tău: {ales_text}. "
                    f"Răspuns corect: {q['variante'][q['corect']]}."
                )
                if q.get("explicatie"):
                    st.caption(_md(q["explicatie"]))
                st.divider()

    st.download_button(
        "Descarcă afirmațiile pentru printat (.html)",
        data=html_quiz(s["intrebari"]),
        file_name="adevarat_fals.html",
        mime="text/html",
        on_click="ignore",
        key="afs_dl",
    )
    b1, b2 = st.columns(2)
    if gresite:
        b1.button(
            "Repetă doar afirmațiile greșite",
            on_click=_repeta_gresite,
            key="afs_repeta",
            use_container_width=True,
        )
    b2.button(
        "Început nou",
        on_click=_inceput_nou,
        key="afs_nou",
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
