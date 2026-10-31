"""Meniul din stânga: logo, profil, Acasă, categoriile pliabile de secțiuni,
Documente și o notă discretă despre Premium."""

import html

import streamlit as st

from abonamente import deschide_abonamente
from limbi import nume_tab, t
from navigare import GRUPE, ICONITE
from utile_pagini import logo_uri, mergi


def _grupe(sectiuni):
    """Grupurile din navigare.py: (cod, iconiță, numele secțiunilor existente)."""
    grupe, folosite = [], set()
    for cod, icoana, nume_membri in GRUPE:
        membri = [s["nume"] for n in nume_membri for s in sectiuni if s["nume"] == n]
        if membri:
            grupe.append((cod, icoana, membri))
            folosite.update(membri)
    ramase = [s["nume"] for s in sectiuni if s["nume"] not in folosite]
    if ramase:
        grupe.append(("altele", "apps", ramase))
    return grupe


def _buton(cheie, eticheta, icoana, pagina, curenta):
    st.button(
        eticheta,
        key=f"meniu_{cheie}",
        icon=f":material/{icoana}:",
        on_click=mergi,
        args=(pagina,),
        type="primary" if pagina == curenta else "secondary",
        use_container_width=True,
    )


def _categorie(eticheta, deschis, icoana):
    """Categorie pliabilă. Dacă versiunea de Streamlit nu știe iconița pe
    expander, se folosește fără iconiță."""
    try:
        return st.expander(eticheta, expanded=deschis, icon=f":material/{icoana}:")
    except TypeError:
        return st.expander(eticheta, expanded=deschis)


def deseneaza_meniu(sectiuni, curenta, deseneaza_profil):
    uri = logo_uri()
    logo = f'<img class="brand-logo" src="{uri}" alt="">' if uri else ""
    with st.sidebar:
        st.markdown(
            f'<div class="brand">{logo}'
            '<span class="brand-nume">AI Study <b>Buddy</b></span></div>',
            unsafe_allow_html=True,
        )
        with st.container(key="profil_lateral"):
            deseneaza_profil()

        with st.container(key="meniu_lateral"):
            _buton("acasa", t("ac.nav.acasa"), "home", "acasa", curenta)
            for i_grup, (cod, icoana, nume_lista) in enumerate(_grupe(sectiuni)):
                with st.container(key=f"grup_{cod}"):
                    with _categorie(
                        t(f"nav.grupa.{cod}"), curenta in nume_lista, icoana
                    ):
                        for i, nume in enumerate(nume_lista):
                            _buton(
                                f"s{i_grup}_{i}",
                                nume_tab(nume),
                                ICONITE.get(nume, "apps"),
                                nume,
                                curenta,
                            )
            _buton(
                "documente",
                t("ac.nav.documente"),
                "folder_open",
                "documente",
                curenta,
            )

        with st.container(key="meniu_premium"):
            st.markdown(
                f'<div class="meniu-prem-t">{html.escape(t("ac.prem.titlu"))}</div>',
                unsafe_allow_html=True,
            )
            if st.button(
                t("ac.prem.btn"),
                key="meniu_prem_btn",
                icon=":material/workspace_premium:",
                use_container_width=True,
            ):
                deschide_abonamente()
