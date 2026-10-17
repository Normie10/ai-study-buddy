"""Memoria aplicației: întrebările și cardurile deja generate se păstrează
într-un „teanc”, separat pentru fiecare persoană care intră în aplicație, ca
să nu vadă aceleași întrebări de două ori în aceeași sesiune."""

import random
import uuid

import streamlit as st

from config import MAX_DOCUMENTE_IN_MEMORIE
from utile import norm


@st.cache_resource
def depozit():
    """Dicționar comun aplicației, cât timp rulează — dar fiecare persoană are
    propriile chei în el, pentru că fiecare cheie include un id de sesiune."""
    return {}


def _id_sesiune():
    """Un identificator unic per persoană (per sesiune de browser), generat o
    singură dată și ținut minte cât timp persoana stă pe pagină."""
    if "id_sesiune" not in st.session_state:
        st.session_state["id_sesiune"] = uuid.uuid4().hex
    return st.session_state["id_sesiune"]


def citeste(cheie):
    """Ce am salvat sub această cheie (sau None)."""
    return depozit().get(cheie)


def salveaza(cheie, valoare):
    """Salvează o valoare; dacă memoria e plină, șterge cea mai veche intrare."""
    dep = depozit()
    if cheie not in dep and len(dep) >= MAX_DOCUMENTE_IN_MEMORIE:
        dep.pop(next(iter(dep)))
    dep[cheie] = valoare


# ------------------------- teancul de elemente -------------------------
def _ia_teanc(cheie):
    dep = depozit()
    if cheie not in dep and len(dep) >= MAX_DOCUMENTE_IN_MEMORIE:
        dep.pop(next(iter(dep)))  # șterge cel mai vechi
    return dep.setdefault(cheie, {"elemente": [], "model": "?"})


def _completeaza_teanc(teanc, genereaza, camp):
    """Face o cerere la Google și adaugă în teanc elementele noi (fără duplicate)."""
    noi, model = genereaza()
    teanc["model"] = model
    existente = {norm(e[camp]) for e in teanc["elemente"]}
    for e in noi:
        if norm(e[camp]) not in existente:
            teanc["elemente"].append(e)
            existente.add(norm(e[camp]))


def _alege_din_teanc(cheie, teanc, nr):
    """Alege nr elemente, cu prioritate pe cele pe care utilizatorul nu le-a mai văzut.
    Întoarce (elemente, au_fost_repetari)."""
    vazute = st.session_state.setdefault("vazute", {}).setdefault(cheie, set())
    n = len(teanc["elemente"])
    libere = [i for i in range(n) if i not in vazute]
    alese = random.sample(libere, min(nr, len(libere)))
    repetate = False
    if len(alese) < nr:
        # nu sunt destule nevăzute: completăm din cele deja văzute
        deja = [i for i in range(n) if i not in alese]
        extra = random.sample(deja, min(nr - len(alese), len(deja)))
        repetate = bool(extra)
        alese += extra
        vazute.clear()
    vazute.update(alese)
    return [dict(teanc["elemente"][i]) for i in alese], repetate


def preia_din_teanc(cheie, nr, camp, genereaza):
    """Întoarce (elemente_alese, model, nota).
    Teancul e propriu persoanei curente (cheia internă include id-ul sesiunii),
    deci persoana următoare care generează primește un teanc nou al ei."""
    cheie_proprie = cheie + (_id_sesiune(),)
    teanc = _ia_teanc(cheie_proprie)
    vazute = st.session_state.setdefault("vazute", {}).setdefault(cheie_proprie, set())
    nevazute = [i for i in range(len(teanc["elemente"])) if i not in vazute]

    nota = "din memorie, fără cerere nouă la Google"
    if len(nevazute) < nr:
        try:
            _completeaza_teanc(teanc, genereaza, camp)
            nota = "cerere nouă la Google"
        except Exception:
            if not teanc["elemente"]:
                raise  # nu avem nimic din memorie, arătăm eroarea
            nota = (
                "Google e aglomerat sau limita e atinsă, "
                "așa că am refolosit elemente din memorie"
            )

    alese, repetate = _alege_din_teanc(cheie_proprie, teanc, nr)
    if repetate:
        nota += " (unele se pot repeta)"
    return alese, teanc["model"], nota


def preia_pentru_examen(cheie, nr, camp, genereaza):
    """Ca preia_din_teanc, dar face o cerere la Google doar dacă teancul (propriu
    persoanei) are mai puține întrebări decât cele cerute."""
    cheie_proprie = cheie + (_id_sesiune(),)
    teanc = _ia_teanc(cheie_proprie)

    nota = "din memorie, fără cerere nouă la Google"
    if len(teanc["elemente"]) < nr and teanc.get("max_cerut", 0) < nr:
        try:
            _completeaza_teanc(teanc, genereaza, camp)
            teanc["max_cerut"] = nr
            nota = "cerere nouă la Google"
        except Exception:
            if not teanc["elemente"]:
                raise
            nota = (
                "Google e aglomerat sau limita e atinsă, "
                "așa că am folosit întrebările din memorie"
            )

    alese, _ = _alege_din_teanc(cheie_proprie, teanc, nr)
    return alese, teanc["model"], nota


def amesteca_variante(q):
    """Amestecă variantele și actualizează indexul răspunsului corect.
    La Adevărat/Fals nu amestecăm: „Adevărat” rămâne mereu prima variantă."""
    if q.get("tip_intrebare") == "af":
        return q
    ordine = list(range(len(q["variante"])))
    random.shuffle(ordine)
    q["variante"] = [q["variante"][i] for i in ordine]
    q["corect"] = ordine.index(q["corect"])
    return q
