"""Secțiune: Progresul meu.

Istoricul scorurilor obținute la Quiz, Examen, SAT, Adevărat/Fals și
Completează. Orice rezultat poate fi marcat cu o steluță (favorit), ca să fie
ușor de găsit printre multe încercări. Poți filtra ce tip de rezultate vezi.
"""

import streamlit as st

from baza_date import progres_utilizator, seteaza_favorit

NUME = "Progresul meu"
ORDINE = 99  # apare ultima, după celelalte secțiuni
CERE_MATERIAL = False
DESCRIERE = (
    "Istoricul scorurilor tale la Quiz, Examen, SAT, Adevărat/Fals și "
    "Completează. Poți marca rezultatele importante cu o steluță și poți "
    "filtra după tip."
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


def afiseaza(ctx):
    st.caption(DESCRIERE)

    try:
        istoric = progres_utilizator()
    except Exception as e:
        st.error(f"Nu am putut încărca progresul: {e}")
        return

    if not istoric:
        st.info("Nu ai niciun rezultat salvat încă. Termină un quiz sau un examen.")
        return

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
