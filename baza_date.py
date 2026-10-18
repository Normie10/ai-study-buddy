"""Conexiunea la Supabase: autentificare (cont, login, logout), materialele
salvate și progresul (scorurile) pe cont. Ține minte sesiunea și după un
refresh de pagină, folosind un cookie cu token-urile de sesiune."""

import datetime
import hashlib
import time

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
    # pauză, ca browserul să apuce efectiv să scrie cookie-ul înainte să
    # continuăm (altfel un rerun imediat după poate „tăia” scrierea)
    time.sleep(0.7)


def _salveaza_sesiune(sesiune):
    """Ține minte utilizatorul în session_state și salvează ambele token-uri
    (acces + reîmprospătare) într-un cookie, ca sesiunea să supraviețuiască
    unui refresh de pagină."""
    st.session_state["utilizator"] = sesiune.user
    _scrie_cookie_sesiune(sesiune.access_token, sesiune.refresh_token)


def incearca_restaureaza_sesiune(cookies):
    """Dacă există un cookie valid (din `cookies`, citit deja de
    toate_cookiurile()) și nimeni nu e logat încă în sesiunea curentă,
    reîncarcă sesiunea."""
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


# ------------------------- cont și autentificare -------------------------
def inregistreaza(email, parola):
    """Creează un cont nou. Întoarce True dacă e nevoie de confirmare prin
    email, False dacă utilizatorul e deja autentificat (fără confirmare)."""
    rezultat = _client().auth.sign_up({"email": email, "password": parola})
    if rezultat.session is not None:
        _salveaza_sesiune(rezultat.session)
        return False
    return True


def autentifica(email, parola):
    rezultat = _client().auth.sign_in_with_password(
        {"email": email, "password": parola}
    )
    _salveaza_sesiune(rezultat.session)


def delogheaza():
    try:
        _client().auth.sign_out()
    except Exception:
        pass
    try:
        _cookie_manager().delete(NUME_COOKIE, key="del_sesiune_cookie")
        time.sleep(0.5)
    except Exception:
        pass
    st.session_state.pop("utilizator", None)
    st.session_state.pop("supabase_client", None)


def utilizator_curent():
    """Întoarce utilizatorul autentificat, sau None."""
    return st.session_state.get("utilizator")


# ------------------------- materialele salvate -------------------------
def salveaza_material(nume, continut):
    user = utilizator_curent()
    hash_continut = hashlib.sha256(continut.encode("utf-8")).hexdigest()[:16]
    _client().table("materiale").insert(
        {
            "user_id": user.id,
            "nume": nume,
            "continut": continut,
            "hash": hash_continut,
        }
    ).execute()


def materiale_utilizator():
    user = utilizator_curent()
    rezultat = (
        _client()
        .table("materiale")
        .select("id, nume, creat_la, continut")
        .eq("user_id", user.id)
        .order("creat_la", desc=True)
        .execute()
    )
    return rezultat.data


def sterge_material(material_id):
    _client().table("materiale").delete().eq("id", material_id).execute()


# ------------------------- progres (scoruri) -------------------------
def salveaza_progres(sectiune, scor, total, detalii=None):
    """Salvează un rezultat (scor/total) pentru utilizatorul curent. Nu
    oprește aplicația dacă eșuează — un scor nesalvat nu trebuie să strice
    afișarea rezultatului către elev."""
    user = utilizator_curent()
    if user is None:
        return
    try:
        _client().table("progres").insert(
            {
                "user_id": user.id,
                "sectiune": sectiune,
                "scor": scor,
                "total": total,
                "detalii": detalii or {},
            }
        ).execute()
    except Exception:
        pass


def progres_utilizator(limita=50):
    user = utilizator_curent()
    rezultat = (
        _client()
        .table("progres")
        .select("id, sectiune, scor, total, creat_la, este_favorit")
        .eq("user_id", user.id)
        .order("creat_la", desc=True)
        .limit(limita)
        .execute()
    )
    return rezultat.data


def seteaza_favorit(progres_id, favorit):
    _client().table("progres").update({"este_favorit": favorit}).eq(
        "id", progres_id
    ).execute()
