"""Mici ajutoare pentru navigarea între pagini (Acasă, Documente, secțiuni)."""

import base64
from pathlib import Path

import streamlit as st

_DIR = Path(__file__).resolve().parent
# se încearcă pe rând: mascota originală, apoi iconița decupată
_FISIERE = ("mascota.png", "avatar_coleg.png")


@st.cache_data(show_spinner=False)
def logo_uri():
    """Mascota, ca text care poate fi pus direct într-o imagine HTML."""
    for nume in _FISIERE:
        try:
            octeti = (_DIR / nume).read_bytes()
        except OSError:
            continue
        return "data:image/png;base64," + base64.b64encode(octeti).decode("ascii")
    return ""


def mergi(pagina):
    """Schimbă pagina curentă (folosit ca on_click la butoane)."""
    st.session_state["pagina"] = pagina
