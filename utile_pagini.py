"""Mici ajutoare pentru navigarea între pagini și pentru imagini."""

import base64
from pathlib import Path

import streamlit as st

_DIR = Path(__file__).resolve().parent


@st.cache_data(show_spinner=False)
def imagine_uri(*nume_fisiere):
    """Prima imagine care există din listă, ca text pentru <img>.
    Dacă nu există niciuna, întoarce text gol."""
    for nume in nume_fisiere:
        try:
            octeti = (_DIR / nume).read_bytes()
        except OSError:
            continue
        return "data:image/png;base64," + base64.b64encode(octeti).decode("ascii")
    return ""


def logo_uri():
    return imagine_uri("mascota.png", "avatar_coleg.png")


def mergi(pagina):
    """Schimbă pagina curentă (folosit ca on_click la butoane)."""
    st.session_state["pagina"] = pagina
