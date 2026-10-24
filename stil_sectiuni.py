"""Stil pentru secțiunile Adevărat/Fals, Completează și Progresul meu."""

import streamlit as st

from stil_taburi import CSS_TABURI

CSS_SECTIUNI = """
<style>
/* ---------- Card de întrebare (peste stilul .fc din flashcarduri) ---------- */
.fc-mic {
    min-height: 8rem;
}
.fc-mic .fc-text {
    font-size: 1.2rem;
    font-weight: 600;
}
/* spațiul liber de la „Completează” */
.fc-gol {
    display: inline-block;
    min-width: 5rem;
    margin: 0 0.25rem;
    border-bottom: 3px solid var(--accent);
}
.fc-gol-plin {
    color: var(--accent);
    font-weight: 800;
}

/* ---------- Butoane late, ușor de apăsat ---------- */
[class*="st-key-afs_adev"] button,
[class*="st-key-afs_fals"] button,
[class*="st-key-afs_next"] button,
[class*="st-key-comp_next"] button {
    min-height: 3rem;
    font-size: 1.02rem;
}

/* ---------- Istoricul din „Progresul meu” ---------- */
.pr-nume {
    font-weight: 700;
}
.pr-data {
    color: var(--muted);
    font-size: 0.8rem;
}
.pr-scor {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border: 1px solid var(--border-hover);
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
}
.pr-scor-bun {
    background: var(--accent-soft);
    border-color: rgba(229, 56, 59, 0.5);
    color: var(--accent);
}
</style>
"""


def injecteaza_stiluri():
    """Stilul flashcardurilor (.fc) plus stilul în plus de aici."""
    st.markdown(CSS_TABURI, unsafe_allow_html=True)
    st.markdown(CSS_SECTIUNI, unsafe_allow_html=True)
