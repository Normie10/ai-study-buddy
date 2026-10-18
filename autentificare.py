"""Ecranul de login / creare cont, afișat înainte de restul aplicației.
Oferă și opțiunea de a continua ca vizitator, fără cont."""

import streamlit as st

from baza_date import autentifica, inregistreaza, intra_ca_vizitator


def ecran_autentificare():
    st.title("AI Study Buddy")
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
