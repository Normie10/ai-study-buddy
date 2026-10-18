"""Conexiunea la Supabase: autentificare (cont, login, logout), materialele
salvate și progresul (scorurile) pe cont. Ține minte sesiunea și după un
refresh de pagină, folosind un cookie cu token-urile de sesiune."""

import datetime
import hashlib

import extra_streamlit_components as stx
import streamlit as st
from supabase import create_client

NUME_COOKIE = "sb_sesiune"


def _cookie_manager():
    """Un singur manager de cookie-uri per sesiune de browser."""
    if "cookie_manager" not in st.session_state:
        st.session_state["cookie_manager"] = stx.CookieManager(key="cm_studybuddy")
    return st.session_state["cookie_manager"]


def toate_cookiurile():
    """Trebuie apelată o singură dată, devreme în pagină, la fiecare rulare —
    dă ocazia managerului să citească cookie-urile din browser."""
    try:
        return _cookie_manager().get_all(key="citeste_toate_cookie") or {}
    except Exception:
        return {}


def _client():
    """Un client Supabase propriu fiecărei sesiuni de browser (nu e comun
    tuturor utilizatorilor, ca să nu se amestece conturile)."""
    if "supabase_client" not in st.session_state:
        url = st.secrets["SUPABASE_URL"]
        cheie = st.secrets["SUPABASE_KEY"]
        st.session_state["supabase_client"] = create_client(url, cheie)
    return st.session_state["supabase_client"]


def _scrie_cookie_sesiune(access_token, refresh_token):
    valoare = f"{access_token}|{refresh_token}"
    _cookie_manager().set(
        NUME_COOKIE,
        valoare,
        expires_at=datetime.datetime.now() + datetime.timedelta(days=30),
        key="set_sesiune_cookie",
    )


def _salveaza_sesiune(sesiune):
    """Ține minte utilizatorul în session_state și salvează ambele token-uri
    (acces + reîmprospătare) într-un cookie, ca sesiunea să supraviețuiască
    unui refresh de pagină."""
    st.session_state["utilizator"] = sesiune.user
    _scrie_cookie_sesiune(sesiune.access_token, sesiune.refresh_token)


def incearca_restaureaza_sesiune(cookies):
    """Dacă există un cookie valid (din `cookies`, citit deja de
    toate_cookiurile()) și nimeni nu e logat încă în sesiunea curentă,
    reîncarcă sesiunea. Folosim set_session (nu refresh_session), ca să NU
    forțăm o rotație de token la fiecare simplă vizionare a paginii —
    Supabase reîmprospătează singur doar când chiar e nevoie."""
    if utilizator_curent() is not None:
        return
    valoare = cookies.get(NUME_COOKIE)
    if not valoare or "|" not in valoare:
        st.session_state["debug_sesiune"] = "fără cookie"
        return
    access_token, refresh_token = valoare.split("|", 1)
    try:
        rezultat = _client().auth.set_session(access_token, refresh_token)
        if rezultat.session is not None:
            st.session_state["utilizator"] = rezultat.session.user
            # dacă Supabase a reîmprospătat singur token-urile, le rescriem
            if (
                rezultat.session.access_token != access_token
                or rezultat.session.refresh_token != refresh_token
            ):
                _scrie_cookie_sesiune(
                    rezultat.session.access_token, rezultat.session.refresh_token
                )
            st.session_state["debug_sesiune"] = "succes"
        else:
            st.session_state["debug_sesiune"] = "răspuns fără sesiune"
    except Exception as e:
        st.session_state["debug_sesiune"] = f"eroare: {e}"


# ------------------------- cont și
