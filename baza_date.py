"""Conexiunea la Supabase: autentificare (cont, login, logout), materialele
salvate și progresul (scorurile) pe cont. Nu folosește deloc interfața
(Streamlit), în afară de session_state, ca să țină minte clientul și
utilizatorul curent."""

import hashlib

import streamlit as st
from supabase import create_client


def _client():
    """Un client Supabase propriu fiecărei sesiuni de browser (nu e comun
    tuturor utilizatorilor, ca să nu se amestece conturile)."""
    if "supabase_client" not in st.session_state:
        url = st.secrets["SUPABASE_URL"]
        cheie = st.secrets["SUPABASE_KEY"]
        st.session_state["supabase_client"] = create_client(url, cheie)
    return st.session_state["supabase_client"]


# ------------------------- cont și autentificare -------------------------
def inregistreaza(email, parola):
    """Creează un cont nou. Întoarce True dacă e nevoie de confirmare prin
    email, False dacă utilizatorul e deja autentificat (fără confirmare)."""
    rezultat = _client().auth.sign_up({"email": email, "password": parola})
    if rezultat.session is not None:
        st.session_state["utilizator"] = rezultat.user
        return False
    return True


def autentifica(email, parola):
    rezultat = _client().auth.sign_in_with_password(
        {"email": email, "password": parola}
    )
    st.session_state["utilizator"] = rezultat.user


def delogheaza():
    try:
        _client().auth.sign_out()
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
