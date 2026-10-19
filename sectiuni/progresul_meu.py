"""Secțiune: Progresul meu.

Istoricul scorurilor obținute la Quiz, Examen, SAT, Adevărat/Fals și
Completează, plus un mic rezumat statistic (total încercări, scor mediu,
grafice). Orice rezultat poate fi marcat cu o steluță (favorit). Poți filtra
ce tip de rezultate vezi. Disponibil doar cu un cont — un vizitator vede un
mesaj explicativ.
"""

import pandas as pd
import streamlit as st

from baza_date import este_vizitator, progres_utilizator, seteaza_favorit

NUME = "Progresul meu"
ORDINE = 99  # apare ultima, după celelalte secțiuni
CERE_MATERIAL = False
DESCRIERE = (
    "Istoricul scorurilor tale la Quiz, Examen, SAT, Adevărat/Fals și "
    "Completează, cu statistici și grafice. Poți marca rezultatele importante "
    "cu o steluță și poți filtra după tip."
)

NUME_SECTIUNE = {
    "quiz": "Quiz",
    "examen": "Examen",
    "sat": "SAT",
    "af": "Adevărat/Fals",
    "comp": "Completează",
}


def _comuta_favorit(rand_id, favorit_nou):
    try:
        seteaza_favorit(rand_id, favorit_nou)
    except Exception as e:
        st.error(f"Nu am putut actualiza: {e}")


def _randeaza(rand):
    nume_sect = NUME_SECTIUNE.get(rand["sectiune"], rand["sectiune"])
    scor, total = rand["scor"], rand["total"]
    procent = round(100 * scor / total) if total else 0
    data = str(rand.get("creat_la", ""))[:16].replace("T", " ")

    c1, c2, c3 = st.columns([3, 1, 1])
    c1.markdown(f"**{nume_sect}** — {data}")
    c2.write(f"{scor}/{total} ({procent}%)")
    steluta = "★" if rand.get("este_favorit") else "☆"
    if c3.button(steluta, key=f"fav_{rand['id']}"):
        _comuta_favorit(rand["id"], not rand.get("este_favorit"))
        st.rerun()


def _statistici(istoric):
    df = pd.DataFrame(istoric)
    df["procent"] = (100 * df["scor"] / df["total"]).round(1)
    df["nume_sectiune"] = df["sectiune"].map(lambda t: NUME_SECTIUNE.get(t, t))
    df["data"] = pd.to_datetime(df["creat_la"])
    df = df.sort_values("data")

    total_incercari = len(df)
    scor_mediu = round(df["procent"].mean())
    preferata = df["nume_sectiune"].value_counts().idxmax()

    st.subheader("Statistici")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total încercări", total_incercari)
    c2.metric("Scor mediu", f"{scor_mediu}%")
    c3.metric("Secțiunea preferată", preferata)

    g1, g2 = st.columns(2)
    with g1:
        st.caption("Încercări pe tip")
        pe_tip = df["nume_sectiune"].value_counts()
        st.bar_chart(pe_tip)
    with g2:
        st.caption("Evoluția scorului (%) în timp")
        serie = df.set_index("data")["procent"]
        st.line_chart(serie)

    st.divider()


def afiseaza(ctx):
    st.caption(DESCRIERE)

    if este_vizitator():
        st.info(
            "Progresul se salvează doar cu un cont. Creează unul gratuit din "
            "colțul din dreapta sus, ca să-ți vezi istoricul aici data viitoare."
        )
        return

    try:
        istoric = progres_utilizator()
    except Exception as e:
        st.error(f"Nu am putut încărca progresul: {e}")
        return

    if not istoric:
        st.info("Nu ai niciun rezultat salvat încă. Termină un quiz sau un examen.")
        return

    _statistici(istoric)

    tipuri_prezente = sorted(
        {r["sectiune"] for r in istoric},
        key=lambda t: list(NUME_SECTIUNE.keys()).index(t) if t in NUME_SECTIUNE else 99,
    )
    optiuni = [NUME_SECTIUNE.get(t, t) for t in tipuri_prezente]
    alese = st.multiselect(
        "Arată doar", optiuni, default=optiuni, key="progres_filtru"
    )
    tipuri_alese = {
        t for t in tipuri_prezente if NUME_SECTIUNE.get(t, t) in alese
    }
    istoric_filtrat = [r for r in istoric if r["sectiune"] in tipuri_alese]

    if not istoric_filtrat:
        st.info("Niciun rezultat pentru filtrul ales.")
        return

    favorite = [r for r in istoric_filtrat if r.get("este_favorit")]
    restul = [r for r in istoric_filtrat if not r.get("este_favorit")]

    if favorite:
        st.subheader("Favorite")
        for rand in favorite:
            _randeaza(rand)
        st.divider()

    st.subheader("Tot istoricul" if favorite else "Istoric")
    for rand in restul:
        _randeaza(rand)
