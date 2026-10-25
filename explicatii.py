"""Explicațiile pentru răspunsurile greșite: de ce varianta aleasă nu e bună."""

import streamlit as st

from limbi import t, varianta_ui
from utile import md


def de_ce_gresit(q, ales):
    """Explicația pentru varianta aleasă greșit, sau None dacă nu există."""
    texte = q.get("de_ce_gresit")
    if not texte or not ales or ales not in q["variante"]:
        return None
    pozitie = q["variante"].index(ales)
    if pozitie >= len(texte):
        return None
    return texte[pozitie] or None


def arata_motiv_greseala(q, ales):
    motiv = de_ce_gresit(q, ales)
    if motiv:
        st.markdown(f"**{t('expl.de_ce')}** {md(motiv, q)}")


def arata_corect_si_motiv(q, ales):
    """Folosită în rezultatele examenului."""
    corect_ui = varianta_ui(q["variante"][q["corect"]], q)
    st.markdown(t("expl.corect", r=md(corect_ui, q)))
    arata_motiv_greseala(q, ales)


def arata_greseala_quiz(i, q, corect, ales):
    """Folosită în Quiz, după predare. `corect` e valoarea internă; doar
    afișarea se traduce."""
    st.error(t("expl.gresit_quiz", i=i + 1, corect=varianta_ui(corect, q)))
    arata_motiv_greseala(q, ales)
