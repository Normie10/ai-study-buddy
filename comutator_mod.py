"""Comutatorul luminos / întunecat: butonul rotund din colțul de sus, dreapta.
Modul ales se ține în sesiune (la reîncărcarea paginii revine la cel implicit)."""

import streamlit as st

# Modul cu care pornește aplicația. Se schimbă în "light" după ce modul
# luminos e verificat pe toate paginile.
MOD_IMPLICIT = "dark"
_CHEIE = "mod_ui"


def mod_ui():
    """'light' sau 'dark' (modul ales acum în această sesiune)."""
    if st.session_state.get(_CHEIE) not in ("light", "dark"):
        st.session_state[_CHEIE] = MOD_IMPLICIT
    return st.session_state[_CHEIE]


def _schimba():
    st.session_state[_CHEIE] = "dark" if mod_ui() == "light" else "light"


def deseneaza_comutator():
    """Butonul arată iconița modului în care treci la apăsare."""
    icoana = "dark_mode" if mod_ui() == "light" else "light_mode"
    with st.container(key="comutator_mod"):
        st.button(
            "Schimbă modul",
            key="comutator_mod_btn",
            icon=f":material/{icoana}:",
            on_click=_schimba,
        )
