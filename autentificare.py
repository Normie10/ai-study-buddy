"""Ecranul de login / creare cont, afișat înainte de restul aplicației.
Aspectul urmează poza de referință (stânga bun venit cu robotul, dreapta
cardul de autentificare). Oferă și opțiunea de a continua ca vizitator, fără
cont, și fluxul de resetare a parolei."""

import html

import streamlit as st

from baza_date import (
    autentifica,
    inregistreaza,
    intra_ca_vizitator,
    seteaza_parola_noua,
    seteaza_sesiune_din_recuperare,
    trimite_email_resetare,
)
from limbi import limba_ui, selector_limba, t
from stil_login import CSS_LOGIN
from utile_pagini import imagine_uri


# ------------------------- mesaje de eroare -------------------------
# (cheia mesajului, fragmente căutate în textul sau codul erorii). Ordinea
# contează: prima potrivire câștigă.
_CATEGORII = [
    ("auth_err_neconfirmat", ("email not confirmed", "email_not_confirmed")),
    ("auth_err_credentiale", ("invalid login credentials", "invalid_credentials")),
    (
        "auth_err_existent",
        ("already registered", "already been registered", "user_already_exists",
         "email_exists"),
    ),
    ("auth_err_parola_aceeasi", ("different from the old", "same_password")),
    ("auth_err_parola_slaba", ("password should be", "weak_password", "at least 6")),
    (
        "auth_err_email_invalid",
        ("invalid email", "email_address_invalid", "unable to validate email",
         "validate email"),
    ),
    (
        "auth_err_limita",
        ("rate limit", "rate_limit", "too many", "over_request_rate_limit",
         "over_email_send_rate_limit", "429"),
    ),
    (
        "auth_err_retea",
        ("connection", "timed out", "timeout", "network", "name resolution",
         "getaddrinfo", "unreachable", "502", "503", "504"),
    ),
]


def _cheie_eroare(exceptie):
    """Alege mesajul potrivit după textul și codul erorii. Ce nu recunoaște
    ajunge la mesajul general."""
    cod = str(getattr(exceptie, "code", "") or "")
    text = f"{cod} {exceptie}".lower()
    for cheie, fragmente in _CATEGORII:
        if any(f in text for f in fragmente):
            return cheie
    nume_tip = type(exceptie).__name__.lower()
    if any(x in nume_tip for x in ("connect", "timeout", "network")):
        return "auth_err_retea"
    return "auth_err_necunoscut"


def arata_eroare_auth(exceptie):
    """Mesajul tradus, plus detaliul tehnic (mic, gri) la erorile de rețea
    sau necunoscute, ca să le putem descoperi în timpul testelor."""
    cheie = _cheie_eroare(exceptie)
    st.error(t(cheie))
    if cheie in ("auth_err_necunoscut", "auth_err_retea"):
        detaliu = str(exceptie).strip()[:200] or type(exceptie).__name__
        st.caption(t("avert.detalii", motiv=detaliu))


# ------------------------- piese comune -------------------------
def _t2(ro, en):
    """Text scurt în limba interfeței (pentru textele noi, fără fișierul de traduceri)."""
    return ro if limba_ui() == "ro" else en


def _forteaza_intunecat():
    """Pagina de login e făcută doar pentru modul întunecat (ca în poză). Dacă
    cineva a lăsat modul luminos pornit și s-a delogat, trecem pe întunecat."""
    if st.session_state.get("mod_ui") == "light":
        st.session_state["mod_ui"] = "dark"
        st.rerun()


def _antet():
    """Antetul simplu (marca + numele aplicației), folosit de ecranul pentru
    parola nouă. HTML-ul rămâne pe UN SINGUR rând, fără linii goale, altfel
    Markdown îl strică."""
    html_antet = (
        '<div class="hero"><div class="hero-marca"></div><div>'
        '<div class="hero-titlu">AI Study Buddy</div>'
        '<div class="hero-sub">' + t("auth_hero_sub") + "</div>"
        "</div></div>"
    )
    st.markdown(html_antet, unsafe_allow_html=True)
    selector_limba()


def _seteaza_mod(mod):
    st.session_state["auth_mod"] = mod


def _panou_stanga():
    """Marca, titlul de bun venit și robotul."""
    logo = imagine_uri("logo_login.png")
    robot = imagine_uri("robot_login.png")
    img_logo = f'<img class="log-logo" src="{logo}" alt="">' if logo else ""
    img_robot = f'<img class="log-robot" src="{robot}" alt="">' if robot else ""
    sus = html.escape(_t2("Bun venit la", "Welcome to"))
    st.markdown(
        '<div class="log-stanga">'
        f'<div class="log-brand">{img_logo}'
        '<div class="log-brand-nume">AI Study<br><b>Buddy</b></div></div>'
        f'<div class="log-titlu">{sus}<br><span>AI Study Buddy!</span></div>'
        f'<div class="log-sub">{html.escape(t("auth_hero_sub"))}</div>'
        f"{img_robot}</div>",
        unsafe_allow_html=True,
    )


def _capul_cardului(titlu, sub):
    logo = imagine_uri("logo_login.png")
    img = f'<img class="log-card-logo" src="{logo}" alt="">' if logo else ""
    st.markdown(
        f'<div class="log-card-cap">{img}'
        f'<div class="log-card-titlu">{html.escape(titlu)}</div>'
        f'<div class="log-card-sub">{html.escape(sub)}</div></div>',
        unsafe_allow_html=True,
    )


# ------------------------- ecrane -------------------------
def ecran_autentificare():
    _forteaza_intunecat()
    st.markdown(CSS_LOGIN, unsafe_allow_html=True)
    st.markdown('<div class="log-marker"></div>', unsafe_allow_html=True)

    stanga, dreapta = st.columns([1.05, 1], gap="large")
    with stanga:
        _panou_stanga()
    with dreapta:
        with st.container(key="log_card"):
            if st.session_state.get("arata_resetare"):
                _formular_cerere_resetare()
            elif st.session_state.get("auth_mod") == "cont_nou":
                _formular_cont_nou()
            else:
                _formular_login()
            st.divider()
            selector_limba()


def _formular_login():
    _capul_cardului(
        _t2("Autentificare", "Sign in"),
        _t2(
            "Intră în contul tău pentru a continua",
            "Sign in to your account to continue",
        ),
    )
    with st.form("form_login"):
        email = st.text_input(
            t("auth_email"),
            key="login_email",
            placeholder=_t2("Email-ul tău", "Your email"),
            label_visibility="collapsed",
        )
        parola = st.text_input(
            t("auth_parola"),
            type="password",
            key="login_parola",
            placeholder=_t2("Parola ta", "Your password"),
            label_visibility="collapsed",
        )
        trimis = st.form_submit_button(
            t("auth_tab_login"), type="primary", use_container_width=True
        )
    if trimis:
        if not email or not parola:
            st.error(t("auth_completeaza_login"))
        else:
            try:
                autentifica(email, parola)
                st.rerun()
            except Exception as e_login:
                arata_eroare_auth(e_login)

    with st.container(key="log_uitat"):
        if st.button(t("auth_uitat"), key="link_resetare"):
            st.session_state["arata_resetare"] = True
            st.rerun()

    st.markdown(
        f'<div class="log-sau">{html.escape(_t2("sau", "or"))}</div>',
        unsafe_allow_html=True,
    )
    with st.container(key="log_oaspete"):
        if st.button(
            t("auth_vizitator_btn"), key="btn_vizitator", use_container_width=True
        ):
            intra_ca_vizitator()
            st.rerun()
    st.markdown(
        f'<div class="log-mic">{html.escape(t("auth_vizitator_info"))}</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="log_alt"):
        st.button(
            _t2("Nu ai cont? Creează unul acum →", "No account? Create one now →"),
            key="catre_cont_nou",
            on_click=_seteaza_mod,
            args=("cont_nou",),
        )


def _formular_cont_nou():
    _capul_cardului(t("auth_tab_cont_nou"), t("auth_intro"))
    with st.form("form_inregistrare"):
        email_n = st.text_input(
            t("auth_email"),
            key="reg_email",
            placeholder=_t2("Email-ul tău", "Your email"),
            label_visibility="collapsed",
        )
        parola_n = st.text_input(
            t("auth_parola_min"),
            type="password",
            key="reg_parola",
            placeholder=t("auth_parola_min"),
            label_visibility="collapsed",
        )
        parola_n2 = st.text_input(
            t("auth_confirma"),
            type="password",
            key="reg_parola2",
            placeholder=t("auth_confirma"),
            label_visibility="collapsed",
        )
        trimis_n = st.form_submit_button(
            t("auth_creeaza"), type="primary", use_container_width=True
        )
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
                arata_eroare_auth(e_reg)

    with st.container(key="log_alt_login"):
        st.button(
            _t2("Ai deja cont? Intră în cont →", "Already have an account? Sign in →"),
            key="catre_login",
            on_click=_seteaza_mod,
            args=("login",),
        )


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
                arata_eroare_auth(e_reset)

    if st.button(t("auth_inapoi_login"), key="inapoi_login"):
        st.session_state.pop("arata_resetare", None)
        st.rerun()


def ecran_parola_noua(access_token, refresh_token):
    """Ecranul în care cineva venit din link-ul de resetare își alege o
    parolă nouă. Rămâne pe acest ecran până apasă explicit butonul de final,
    indiferent de rerun-urile automate declanșate pe parcurs (de exemplu la
    scrierea cookie-ului de sesiune)."""
    _forteaza_intunecat()
    st.markdown(CSS_LOGIN, unsafe_allow_html=True)
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
                arata_eroare_auth(e_pn)
