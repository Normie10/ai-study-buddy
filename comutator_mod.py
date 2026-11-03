"""Comutatorul luminos / întunecat: un buton în meniul lateral, sub „Documente".
Modul ales se ține în sesiune (la reîncărcarea paginii revine la cel implicit)."""

import streamlit as st

from limbi import limba_ui

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
    """Butonul arată modul în care treci la apăsare. Se desenează în meniul
    lateral, în containerul „meniu_lateral", ca să arate ca restul meniului."""
    ro = limba_ui() == "ro"
    if mod_ui() == "light":
        eticheta = "Mod întunecat" if ro else "Dark mode"
        icoana = "dark_mode"
    else:
        eticheta = "Mod luminos" if ro else "Light mode"
        icoana = "light_mode"
    with st.container(key="mod_luminos"):
        st.button(
            eticheta,
            key="mod_luminos_btn",
            icon=f":material/{icoana}:",
            on_click=_schimba,
            use_container_width=True,
        )
