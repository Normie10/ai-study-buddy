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
from limbi import selector_limba, t


def _antet():
    """Antetul comun: marca roșie + numele aplicației, apoi selectorul de
    limbă. HTML-ul rămâne pe UN SINGUR rând, fără linii goale, altfel
    Markdown îl strică."""
    html_antet = (
        '<div class="hero"><div class="hero-marca"></div><div>'
        '<div class="hero-titlu">AI Study Buddy</div>'
        '<div class="hero-sub">' + t("auth_hero_sub") + "</div>"
        "</div></div>"
    )
    st.markdown(html_antet, unsafe_allow_html=True)
    selector_limba()


def ecran_autentificare():
    _antet()

    if st.session_state.get("arata_resetare"):
        _formular_cerere_resetare()
        return

    st.caption(t("auth_intro"))

    tab_login, tab_inregistrare = st.tabs(
        [t("auth_tab_login"), t("auth_tab_cont_nou")]
    )

    with tab_login:
        with st.form("form_login"):
            email = st.text_input(t("auth_email"), key="login_email")
            parola = st.text_input(
                t("auth_parola"), type="password", key="login_parola"
            )
            trimis = st.form_submit_button(t("auth_tab_login"), type="primary")
        if trimis:
            if not email or not parola:
                st.error(t("auth_completeaza_login"))
            else:
                try:
                    autentifica(email, parola)
                    st.rerun()
                except Exception:
                    st.error(t("auth_login_gresit"))

        if st.button(t("auth_uitat"), key="link_resetare"):
            st.session_state["arata_resetare"] = True
            st.rerun()

    with tab_inregistrare:
        with st.form("form_inregistrare"):
            email_n = st.text_input(t("auth_email"), key="reg_email")
            parola_n = st.text_input(
                t("auth_parola_min"), type="password", key="reg_parola"
            )
            parola_n2 = st.text_input(
                t("auth_confirma"), type="password", key="reg_parola2"
            )
            trimis_n = st.form_submit_button(t("auth_creeaza"), type="primary")
        if trimis_n:
            if not email_n or not parola_n:
                st.error(t("auth_completeaza_toate"))
            elif parola_n != parola_n2:
                st.error(t("auth_parole_diferite"))
            elif len(parola_n) < 6:
                st.error(t("auth_parola_scurta"))
            else:
                try:
                    cere_confirmare = inregistreaza(email_n, parola_n)
                    if cere_confirmare:
                        st.success(t("auth_cont_creat"))
                    else:
                        st.rerun()
                except Exception as e_reg:
                    st.error(t("auth_eroare_cont", eroare=e_reg))

    st.divider()
    st.caption(t("auth_vizitator_info"))
    if st.button(t("auth_vizitator_btn")):
        intra_ca_vizitator()
        st.rerun()


def _formular_cerere_resetare():
    st.subheader(t("auth_reset_titlu"))
    st.caption(t("auth_reset_info"))
    with st.form("form_cerere_resetare"):
        email = st.text_input(t("auth_email"), key="reset_email")
        trimis = st.form_submit_button(t("auth_reset_trimite"), type="primary")
    if trimis:
        if not email:
            st.error(t("auth_reset_scrie_email"))
        else:
            try:
                trimite_email_resetare(email)
                st.success(t("auth_reset_ok"))
            except Exception as e_reset:
                st.error(t("auth_reset_eroare", eroare=e_reset))

    if st.button(t("auth_inapoi_login"), key="inapoi_login"):
        st.session_state.pop("arata_resetare", None)
        st.rerun()


def ecran_parola_noua(access_token, refresh_token):
    """Ecranul în care cineva venit din link-ul de resetare își alege o
    parolă nouă. Rămâne pe acest ecran până apasă explicit butonul de final,
    indiferent de rerun-urile automate declanșate pe parcurs (de exemplu la
    scrierea cookie-ului de sesiune)."""
    _antet()
    st.subheader(t("auth_pn_titlu"))

    if not st.session_state.get("sesiune_recuperare_activa"):
        ok = seteaza_sesiune_din_recuperare(access_token, refresh_token)
        if not ok:
            st.error(t("auth_pn_invalid"))
            return
        st.session_state["sesiune_recuperare_activa"] = True

    if st.session_state.get("parola_schimbata"):
        st.success(t("auth_pn_ok"))
        if st.button(t("auth_pn_continua"), key="continua_dupa_resetare"):
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
            t("auth_pn_parola"), type="password", key="pn_parola"
        )
        parola_noua2 = st.text_input(
            t("auth_pn_confirma"), type="password", key="pn_parola2"
        )
        trimis = st.form_submit_button(t("auth_pn_salveaza"), type="primary")

    if trimis:
        if parola_noua != parola_noua2:
            st.error(t("auth_parole_diferite"))
        elif len(parola_noua) < 6:
            st.error(t("auth_parola_scurta"))
        else:
            try:
                seteaza_parola_noua(parola_noua)
                st.session_state["parola_schimbata"] = True
                st.rerun()
            except Exception as e_pn:
                st.error(t("auth_pn_eroare", eroare=e_pn))
