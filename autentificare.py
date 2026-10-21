"""Ecranul de login / creare cont, afișat înainte de restul aplicației.
Oferă și opțiunea de a continua ca vizitator, fără cont, și fluxul de
resetare a parolei."""

import streamlit as st

from baza_date import (
    autentifica,
    inregistreaza,
    intra_ca_vizitator,
    seteaza_parola_noua,
    seteaza_sesiune_din_recuperare,
    trimite_email_resetare,
)
from config import HERO_HTML


def _antet():
    """Antetul comun: marca roșie + numele aplicației."""
    st.markdown(HERO_HTML, unsafe_allow_html=True)


def ecran_autentificare():
    _antet()

    if st.session_state.get("arata_resetare"):
        _formular_cerere_resetare()
        return

    st.caption(
        "Intră în cont sau creează unul gratuit, ca să-ți salvezi progresul "
        "și materialele."
    )

    tab_login, tab_inregistrare = st.tabs(["Intră în cont", "Cont nou"])

    with tab_login:
        with st.form("form_login"):
            email = st.text_input("Email", key="login_email")
            parola = st.text_input("Parolă", type="password", key="login_parola")
            trimis = st.form_submit_button("Intră în cont", type="primary")
        if trimis:
            if not email or not parola:
                st.error("Completează email și parolă.")
            else:
                try:
                    autentifica(email, parola)
                    st.rerun()
                except Exception:
                    st.error("Email sau parolă greșite.")

        if st.button("Ai uitat parola?", key="link_resetare"):
            st.session_state["arata_resetare"] = True
            st.rerun()

    with tab_inregistrare:
        with st.form("form_inregistrare"):
            email_n = st.text_input("Email", key="reg_email")
            parola_n = st.text_input(
                "Parolă (minimum 6 caractere)", type="password", key="reg_parola"
            )
            parola_n2 = st.text_input(
                "Confirmă parola", type="password", key="reg_parola2"
            )
            trimis_n = st.form_submit_button("Creează cont", type="primary")
        if trimis_n:
            if not email_n or not parola_n:
                st.error("Completează toate câmpurile.")
            elif parola_n != parola_n2:
                st.error("Parolele nu coincid.")
            elif len(parola_n) < 6:
                st.error("Parola trebuie să aibă cel puțin 6 caractere.")
            else:
                try:
                    cere_confirmare = inregistreaza(email_n, parola_n)
                    if cere_confirmare:
                        st.success(
                            "Cont creat! Verifică-ți emailul pentru confirmare, "
                            "apoi intră în cont din tab-ul alăturat."
                        )
                    else:
                        st.rerun()
                except Exception as e_reg:
                    st.error(f"Nu am putut crea contul: {e_reg}")

    st.divider()
    st.caption(
        "Preferi să încerci fără cont? Poți oricând să-ți faci unul mai "
        "târziu, dar materialele și progresul nu se vor salva."
    )
    if st.button("Continuă fără cont"):
        intra_ca_vizitator()
        st.rerun()


def _formular_cerere_resetare():
    st.subheader("Resetează parola")
    st.caption("Scrie emailul contului tău. Îți trimitem un link de resetare.")
    with st.form("form_cerere_resetare"):
        email = st.text_input("Email", key="reset_email")
        trimis = st.form_submit_button("Trimite link-ul", type="primary")
    if trimis:
        if not email:
            st.error("Scrie un email.")
        else:
            try:
                trimite_email_resetare(email)
                st.success(
                    "Dacă există un cont cu acest email, ai primit un link de "
                    "resetare. Verifică și folderul de spam."
                )
            except Exception as e:
                st.error(f"Nu am putut trimite emailul: {e}")

    if st.button("Înapoi la login", key="inapoi_login"):
        st.session_state.pop("arata_resetare", None)
        st.rerun()


def ecran_parola_noua(access_token, refresh_token):
    """Ecranul în care cineva venit din link-ul de resetare își alege o
    parolă nouă. Rămâne pe acest ecran până apasă explicit butonul de final,
    indiferent de rerun-urile automate declanșate pe parcurs (de exemplu la
    scrierea cookie-ului de sesiune)."""
    _antet()
    st.subheader("Setează o parolă nouă")

    if not st.session_state.get("sesiune_recuperare_activa"):
        ok = seteaza_sesiune_din_recuperare(access_token, refresh_token)
        if not ok:
            st.error(
                "Link-ul nu mai este valid (poate a expirat sau a fost deja "
                "folosit). Cere unul nou din ecranul de login."
            )
            return
        st.session_state["sesiune_recuperare_activa"] = True

    if st.session_state.get("parola_schimbata"):
        st.success("Parola a fost schimbată. Poți continua direct în cont.")
        if st.button("Continuă în aplicație", key="continua_dupa_resetare"):
            for cheie in (
                "in_recuperare_parola",
                "recuperare_access_token",
                "recuperare_refresh_token",
                "sesiune_recuperare_activa",
                "parola_schimbata",
            ):
                st.session_state.pop(cheie, None)
            st.rerun()
        return

    with st.form("form_parola_noua"):
        parola_noua = st.text_input(
            "Parolă nouă (minimum 6 caractere)", type="password", key="pn_parola"
        )
        parola_noua2 = st.text_input(
            "Confirmă parola nouă", type="password", key="pn_parola2"
        )
        trimis = st.form_submit_button("Salvează parola nouă", type="primary")

    if trimis:
        if parola_noua != parola_noua2:
            st.error("Parolele nu coincid.")
        elif len(parola_noua) < 6:
            st.error("Parola trebuie să aibă cel puțin 6 caractere.")
        else:
            try:
                seteaza_parola_noua(parola_noua)
                st.session_state["parola_schimbata"] = True
                st.rerun()
            except Exception as e:
                st.error(f"Nu am putut schimba parola: {e}")
