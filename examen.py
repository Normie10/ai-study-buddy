"""Testul cu cronometru. Același cod merge și pentru examenul din document,
și pentru testul SAT."""

import time

import streamlit as st

from baza_date import salveaza_progres
from export_html import html_examen
from explicatii import arata_corect_si_motiv
from utile import eticheta_grup, formateaza_timp, md, sursa_text, text_intrebare


def afiseaza_intrebare(q, i, cheie):
    if q.get("pasaj"):
        with st.container(border=True):
            st.markdown(md(q["pasaj"], q))
    st.radio(
        md(f"{i + 1}. {text_intrebare(q)}", q),
        q["variante"],
        index=None,
        key=cheie,
        format_func=lambda v, q=q: md(v, q),
    )


def sterge_chei_examen(nume):
    """Șterge răspunsurile selectate în testul anterior."""
    prefix = f"{nume}_r"
    for k in list(st.session_state.keys()):
        if k.startswith(prefix) and k[len(prefix):].isdigit():
            del st.session_state[k]


def incheie_examen(nume, expirat=False):
    ex = st.session_state.get(nume)
    if ex and ex["stare"] == "in_curs":
        ex["raspunsuri"] = {
            i: st.session_state.get(f"{nume}_r{i}")
            for i in range(len(ex["intrebari"]))
        }
        ex["sfarsit"] = time.time()
        ex["expirat"] = expirat
        ex["stare"] = "terminat"


def examen_nou(nume):
    sterge_chei_examen(nume)
    st.session_state.pop(nume, None)


def reface_cu_greseli(nume, ex, gresite):
    """Pornește un test nou, doar cu întrebările greșite la ultima predare.
    Timpul alocat e proporțional cu numărul de întrebări greșite."""
    sterge_chei_examen(nume)
    total_initial = len(ex["intrebari"])
    durata_noua = max(60, round(ex["durata"] * len(gresite) / total_initial))
    st.session_state[nume] = {
        "sursa": ex.get("sursa"),
        "titlu": f"Recapitulare greșeli - {ex.get('titlu', 'Rezultate')}",
        "intrebari": list(gresite),
        "cerute": len(gresite),
        "durata": durata_noua,
        "info": "Recapitulare greșeli",
        "context": ex["context"],
        "stare": "in_curs",
        "start": time.time(),
    }


@st.fragment(run_every=1)
def cronometru(nume):
    """Se reîncarcă singur în fiecare secundă; la 0 predă testul."""
    ex = st.session_state.get(nume)
    if not ex or ex["stare"] != "in_curs":
        return
    ramas = ex["durata"] - (time.time() - ex["start"])
    if ramas <= 0:
        incheie_examen(nume, expirat=True)
        st.rerun()
    st.metric("Timp rămas", formateaza_timp(ramas))
    if ramas <= 60:
        st.warning("Mai ai sub un minut!")


def afiseaza_rezultat(ex, nume):
    intrebari = ex["intrebari"]
    total = len(intrebari)
    scor = 0
    grupuri = {}  # etichetă (pagină sau temă) -> [total, greșite]
    detalii = []

    for i, q in enumerate(intrebari):
        ales = ex["raspunsuri"].get(i)
        ok = ales == q["variante"][q["corect"]]
        if ok:
            scor += 1
        stat = grupuri.setdefault(eticheta_grup(q), [0, 0])
        stat[0] += 1
        if not ok:
            stat[1] += 1
        detalii.append((i, q, ales, ok))

    # salvăm scorul pe cont o singură dată, prima oară când se afișează rezultatul
    if not ex.get("progres_salvat"):
        salveaza_progres(nume, scor, total)
        ex["progres_salvat"] = True

    procent = round(100 * scor / total)
    folosit = ex["sfarsit"] - ex["start"]
    fara_raspuns = sum(1 for _, _, ales, _ in detalii if ales is None)
    este_sat = ex.get("sursa") == "sat"

    if ex.get("expirat"):
        st.warning("Timpul a expirat. Întrebările fără răspuns au fost socotite greșite.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Scor", f"{scor}/{total}")
    c2.metric("Procent", f"{procent}%")
    c3.metric("Timp folosit", formateaza_timp(folosit))
    if fara_raspuns:
        st.caption(f"Ai lăsat {fara_raspuns} întrebări fără răspuns.")

    st.subheader("Ce să recapitulezi")
    de_recapitulat = sorted(
        [(eticheta, t, g) for eticheta, (t, g) in grupuri.items() if g > 0],
        key=lambda x: (-x[2], -x[2] / x[1]),
    )
    if not de_recapitulat:
        st.success("Ai răspuns corect la toate întrebările. Bravo!")
    else:
        for eticheta, t, g in de_recapitulat:
            cuvinte = "întrebare greșită" if t == 1 else "întrebări greșite"
            st.markdown(f"- **{eticheta}**: {g} din {t} {cuvinte}")
        if este_sat:
            st.caption("Temele sunt cele atribuite de model fiecărei întrebări.")
        else:
            st.caption(
                "Locurile indicate sunt cele date de model pentru fiecare întrebare. "
                "Verifică-le în document."
            )
    if este_sat:
        st.caption(
            "Întrebările sunt scrise de AI și pot conține greșeli. Scorul nu este "
            "scorul oficial SAT."
        )

    gresite_intrebari = [q for _, q, _, ok in detalii if not ok]
    if gresite_intrebari:
        st.button(
            f"Recapitulează doar greșelile ({len(gresite_intrebari)})",
            on_click=reface_cu_greseli,
            args=(nume, ex, gresite_intrebari),
            key=f"recap_{nume}",
            type="primary",
        )

    with st.expander("Vezi toate întrebările și răspunsurile"):
        for i, q, ales, ok in detalii:
            stare = "Corect" if ok else "Greșit"
            if q.get("pasaj"):
                st.markdown(md(q["pasaj"], q))
            st.markdown(f"**{i + 1}. {md(text_intrebare(q), q)}**")
            st.markdown(
                f"{stare}. Răspunsul tău: {md(ales, q) if ales else 'fără răspuns'}"
            )
            if not ok:
               arata_corect_si_motiv(q, ales)
            st.caption(f"{md(q['explicatie'], q)} ({sursa_text(q)})")
            st.divider()

    st.download_button(
        "Descarcă rezultatele pentru printat (.html)",
        data=html_examen(
            ex.get("titlu", "Rezultate examen"),
            scor,
            total,
            procent,
            folosit,
            de_recapitulat,
            detalii,
            mathjax=este_sat,
        ),
        file_name=f"{nume}_rezultate.html",
        mime="text/html",
        on_click="ignore",
        key=f"dl_{nume}",
    )
    st.button("Examen nou", on_click=examen_nou, args=(nume,), key=f"nou_{nume}")


def afiseaza_examen(nume, context, formular):
    """Gestionează cele trei stări ale unui test: setări, în curs, terminat.
    `context` identifică materialul; dacă se schimbă, testul se resetează.
    `formular()` desenează setările și, când se apasă Începe, întoarce un
    dicționar cu testul (altfel None)."""
    ex = st.session_state.get(nume)
    if ex and ex["context"] != context:
        sterge_chei_examen(nume)
        st.session_state.pop(nume, None)
        ex = None

    if ex is None:
        nou = formular()
        if nou:
            sterge_chei_examen(nume)
            nou["context"] = context
            nou["stare"] = "in_curs"
            nou["start"] = time.time()  # pornește după generare
            st.session_state[nume] = nou
            st.rerun()

    elif ex["stare"] == "in_curs":
        if time.time() - ex["start"] >= ex["durata"]:
            incheie_examen(nume, expirat=True)
            st.rerun()

        cronometru(nume)
        st.caption(f"Model: {ex['info']}")
        if len(ex["intrebari"]) < ex["cerute"]:
            st.info(
                f"Am găsit doar {len(ex['intrebari'])} întrebări distincte, "
                "așa că testul are mai puține decât ai cerut."
            )
        for i, q in enumerate(ex["intrebari"]):
            afiseaza_intrebare(q, i, f"{nume}_r{i}")
        st.button(
            "Predă examenul",
            on_click=incheie_examen,
            args=(nume,),
            key=f"preda_{nume}",
        )

    else:  # terminat
        afiseaza_rezultat(ex, nume)
