"""Secțiune: Progresul meu.

Istoricul scorurilor obținute la Quiz, Examen, SAT, Adevărat/Fals și
Completează, plus un mic rezumat statistic (total încercări, scor mediu,
grafice). Orice rezultat poate fi marcat cu o steluță (favorit). Poți filtra
ce tip de rezultate vezi. Disponibil doar cu un cont — un vizitator vede un
mesaj explicativ.
"""

import html

import pandas as pd
import streamlit as st

from baza_date import este_vizitator, progres_utilizator, seteaza_favorit
from limbi import descriere_sectiune, limba_ui, t
from stil_sectiuni import injecteaza_stiluri

NUME = "Progresul meu"
ORDINE = 99  # apare ultima, după celelalte secțiuni
CERE_MATERIAL = False
DESCRIERE = (
    "Istoricul scorurilor tale la Quiz, Examen, SAT, Adevărat/Fals și "
    "Completează, cu statistici și grafice. Poți marca rezultatele importante "
    "cu o steluță și poți filtra după tip."
)

# codurile salvate în baza de date, în ordinea afișării
ORDINE_TIPURI = ["quiz", "examen", "sat", "af", "comp"]

# Culoarea graficelor. Pune None dacă le preferi în albastrul implicit.
CULOARE_GRAFIC = "#E5383B"


def _nume_tip(cod):
    """Numele afișat pentru un tip de rezultat (sau codul, dacă e necunoscut)."""
    cheie = f"pr.tip.{cod}"
    nume = t(cheie)
    return cod if nume == cheie else nume


def _data_locala(valoare):
    """Data salvată (în UTC) afișată în ora României."""
    try:
        timp = pd.to_datetime(valoare, utc=True).tz_convert("Europe/Bucharest")
        return timp.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(valoare)[:16].replace("T", " ")


def _comuta_favorit(rand_id, favorit_nou):
    try:
        seteaza_favorit(rand_id, favorit_nou)
    except Exception as e:
        st.error(t("pr.eroare_update", e=e))


def _randeaza(rand):
    scor, total = rand["scor"], rand["total"]
    procent = round(100 * scor / total) if total else 0
    clasa = "pr-scor pr-scor-bun" if procent >= 80 else "pr-scor"

    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1.6, 0.8])
        c1.markdown(
            f'<div class="pr-nume">{html.escape(_nume_tip(rand["sectiune"]))}</div>'
            f'<div class="pr-data">{html.escape(_data_locala(rand.get("creat_la", "")))}</div>',
            unsafe_allow_html=True,
        )
        c2.markdown(
            f'<span class="{clasa}">{scor}/{total} · {procent}%</span>',
            unsafe_allow_html=True,
        )
        steluta = "★" if rand.get("este_favorit") else "☆"
        if c3.button(
            steluta, key=f"fav_{rand['id']}", help=t("pr.favorit_ajutor")
        ):
            _comuta_favorit(rand["id"], not rand.get("este_favorit"))
            st.rerun()


def _statistici(istoric):
    df = pd.DataFrame(istoric)
    df["procent"] = (100 * df["scor"] / df["total"]).round(1)
    df["nume_sectiune"] = df["sectiune"].map(_nume_tip)
    df["data"] = pd.to_datetime(df["creat_la"])
    df = df.sort_values("data")

    total_incercari = len(df)
    scor_mediu = round(df["procent"].mean())
    preferata = df["nume_sectiune"].value_counts().idxmax()

    st.subheader(t("pr.statistici"))
    c1, c2, c3 = st.columns(3)
    c1.metric(t("pr.total"), total_incercari)
    c2.metric(t("pr.scor_mediu"), f"{scor_mediu}%")
    c3.metric(t("pr.preferata"), preferata)

    g1, g2 = st.columns(2)
    with g1:
        st.caption(t("pr.grafic_tip"))
        pe_tip = df["nume_sectiune"].value_counts()
        st.bar_chart(pe_tip, color=CULOARE_GRAFIC)
    with g2:
        st.caption(t("pr.grafic_timp"))
        serie = df.set_index("data")["procent"]
        st.line_chart(serie, color=CULOARE_GRAFIC)


def _istoric(istoric):
    tipuri_prezente = sorted(
        {r["sectiune"] for r in istoric},
        key=lambda cod: ORDINE_TIPURI.index(cod) if cod in ORDINE_TIPURI else 99,
    )
    optiuni = [_nume_tip(cod) for cod in tipuri_prezente]
    alese = st.multiselect(
        t("pr.filtru"),
        optiuni,
        default=optiuni,
        key=f"progres_filtru_{limba_ui()}",
    )
    tipuri_alese = {cod for cod in tipuri_prezente if _nume_tip(cod) in alese}
    istoric_filtrat = [r for r in istoric if r["sectiune"] in tipuri_alese]

    if not istoric_filtrat:
        st.info(t("pr.filtru_gol"))
        return

    favorite = [r for r in istoric_filtrat if r.get("este_favorit")]
    restul = [r for r in istoric_filtrat if not r.get("este_favorit")][:50]

    if favorite:
        st.subheader(t("pr.favorite"))
        for rand in favorite:
            _randeaza(rand)

    st.subheader(t("pr.tot") if favorite else t("pr.istoric"))
    for rand in restul:
        _randeaza(rand)


def afiseaza(ctx):
    injecteaza_stiluri()
    st.caption(descriere_sectiune(NUME, DESCRIERE))

    if este_vizitator():
        st.info(t("pr.vizitator"))
        return

    try:
        istoric = progres_utilizator(limita=1000)
    except Exception as e:
        st.error(t("pr.eroare_incarcare", e=e))
        return

    if not istoric:
        st.info(t("pr.gol"))
        return

    with st.container(key="nav_sub_progres"):
        tab_general, tab_istoric = st.tabs(
            [t("pr.tab.general"), t("pr.tab.istoric")]
        )
    with tab_general:
        _statistici(istoric)
    with tab_istoric:
        _istoric(istoric)
