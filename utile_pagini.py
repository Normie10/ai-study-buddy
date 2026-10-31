"""Mici ajutoare pentru navigarea între pagini (Acasă, Documente, secțiuni)."""

import base64
from pathlib import Path

import streamlit as st

_AVATAR = Path(__file__).resolve().parent / "avatar_coleg.png"


@st.cache_data(show_spinner=False)
def logo_uri():
    """Logo-ul, ca text care poate fi pus direct într-o imagine HTML."""
    try:
        octeti = _AVATAR.read_bytes()
    except OSError:
        return ""
    return "data:image/png;base64," + base64.b64encode(octeti).decode("ascii")


def mergi(pagina):
    """Schimbă pagina curentă (folosit ca on_click la butoane)."""
    st.session_state["pagina"] = pagina
