"""Secțiune: Harta conceptelor.

Ideile principale din material, ca o hartă: concepte legate prin săgeți cu
etichete. Harta se cere o singură dată la Google pentru același material și
se păstrează în memorie.
"""

import textwrap

import streamlit as st

from generare_harta import MAX_NODURI, MIN_NODURI, genereaza_harta
from limbi import descriere_sectiune, t
from memorie import citeste, salveaza
from stil_sectiuni import injecteaza_stiluri

NUME = "Harta conceptelor"
ORDINE = 55
CERE_MATERIAL = True
DESCRIERE = (
    "Ideile principale din materialul tău, ca o hartă: concepte legate prin "
    "săgeți cu etichete. O privești și vezi cum se leagă lucrurile între ele."
)

CHEIE = "hr_sesiune"
MIN_CONCEPTE = 5


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _dot_text(text, latime=18):
    """Text sigur pentru desen: fără ghilimele și backslash, pe mai multe rânduri."""
    text = " ".join(str(text).split())
    text = text.replace("\\", "").replace('"', "'")
    return "\\n".join(textwrap.wrap(text, latime)) or " "


def _dot(harta):
    linii = [
        "digraph G {",
        'bgcolor="transparent";',
        'rankdir="TB";',
        "nodesep=0.4;",
        "ranksep=0.6;",
        'node [shape=box, style="rounded,filled", fillcolor="#1E1E24", '
        'color="#E5383B", fontcolor="#F2F2F4", fontname="Helvetica", '
        'fontsize=12, margin="0.18,0.1"];',
        'edge [color="#9B9BA1", fontcolor="#C8C8CE", fontname="Helvetica", '
        "fontsize=10, arrowsize=0.8];",
    ]
    for i, eticheta in enumerate(harta["noduri"]):
        linii.append(f'n{i} [label="{_dot_text(eticheta)}"];')
    for l in harta["legaturi"]:
        if l["eticheta"]:
            linii.append(
                f'n{l["de_la"]} -> n{l["la"]} [label="{_dot_text(l["eticheta"], 14)}"];'
            )
        else:
            linii.append(f'n{l["de_la"]} -> n{l["la"]};')
    linii.append("}")
    return "\n".join(linii)


def _deseneaza(harta):
    try:
        try:
            st.graphviz_chart(_dot(harta), use_container_width=True)
        except TypeError:  # versiune de Streamlit fără acest parametru
            st.graphviz_chart(_dot(harta))
    except Exception:
        st.warning(t("hr.eroare_desen"))


def _afiseaza_harta(s):
    harta = s["harta"]
    if harta.get("titlu"):
        st.subheader(_md(harta["titlu"]))
    st.caption(t("comun.model", info=s["info"]))
    _deseneaza(harta)
    st.caption(t("hr.avertisment"))
    with st.expander(t("hr.legaturi")):
        for l in harta["legaturi"]:
            a = _md(harta["noduri"][l["de_la"]])
            b = _md(harta["noduri"][l["la"]])
            verb = _md(l["eticheta"]) if l["eticheta"] else "→"
            st.markdown(f"- **{a}** — {verb} — **{b}**")


def afiseaza(ctx):
    """Funcția pe care o apelează aplicația pentru această secțiune."""
    injecteaza_stiluri()
    st.caption(descriere_sectiune(NUME, DESCRIERE))

    with st.container(border=True):
        nr = st.number_input(t("hr.nr"), MIN_CONCEPTE, MAX_NODURI, 8, key="hr_nr")
        genereaza = st.button(
            t("hr.genereaza"),
            key="hr_gen",
            type="primary",
            use_container_width=True,
        )

    if genereaza:
        cheie = ("harta", ctx.hash_material, ctx.limba, int(nr))
        salvat = citeste(cheie)
        if salvat is not None:
            st.session_state[CHEIE] = {
                "hash": ctx.hash_material,
                "harta": salvat["harta"],
                "info": f"{salvat['model']} · {t('comun.din_memorie')}",
            }
        else:
            with st.spinner(t("hr.spinner")):
                try:
                    harta, model = genereaza_harta(
                        ctx.client, ctx.selectate, ctx.eticheta, int(nr), ctx.limba
                    )
                    salveaza(cheie, {"harta": harta, "model": model})
                    st.session_state[CHEIE] = {
                        "hash": ctx.hash_material,
                        "harta": harta,
                        "info": f"{model} · {t('comun.cerere_noua')}",
                    }
                except Exception as e_hr:
                    st.error(t("comun.eroare", e=e_hr))

    s = st.session_state.get(CHEIE)
    if s and s["hash"] != ctx.hash_material:
        st.session_state.pop(CHEIE, None)  # s-a schimbat materialul
        s = None
    if s:
        _afiseaza_harta(s)
