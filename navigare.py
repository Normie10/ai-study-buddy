"""Navigarea aplicației: secțiunile sunt grupate în trei taburi mari
(Exersează, Învață, Progres). În grupurile cu mai multe secțiuni, fiecare
secțiune are un tab mic, în formă de pastilă. Funcția întoarce câte un tab
pentru fiecare secțiune, în aceeași ordine, ca restul aplicației să le
completeze ca înainte."""

import streamlit as st

from limbi import nume_tab, t

FOLOSESTE_ICONITE = True  # False = taburi fără iconițe, dacă nu se afișează bine

# (cod grup, iconiță, secțiunile din grup, în ordinea afișării)
GRUPE = [
    (
        "exerseaza",
        "fitness_center",
        ["Quiz", "Examen", "Adevărat / Fals", "Găsește greșeala", "Potrivește perechile", "Completează", "SAT"],
    ),
    ("invata", "menu_book", ["Flashcarduri", "Rezumat", "Harta conceptelor", "Întreabă", "Predă-mi tu", "Plan de studiu"]),
    ("progres", "insights", ["Progresul meu"]),
]

ICONITE = {
    "Quiz": "quiz",
    "Examen": "timer",
    "Adevărat / Fals": "fact_check",
    "Completează": "edit_note",
    "SAT": "school",
    "Găsește greșeala": "find_in_page",
    "Potrivește perechile": "compare_arrows",
    "Flashcarduri": "style",
    "Rezumat": "summarize",
    "Întreabă": "forum",
    "Harta conceptelor": "account_tree",
    "Plan de studiu": "calendar_month",
    "Predă-mi tu": "record_voice_over",
    "Progresul meu": "insights",
}

NUME_CUNOSCUTE = {nume for _, _, membri in GRUPE for nume in membri}


def _eticheta(icoana, text):
    if FOLOSESTE_ICONITE and icoana:
        return f":material/{icoana}: {text}"
    return text


def taburi_grupate(sectiuni):
    grupe = []
    folosite = set()
    for cod, icoana, nume_membri in GRUPE:
        membri = [s for n in nume_membri for s in sectiuni if s["nume"] == n]
        if membri:
            grupe.append((cod, icoana, membri))
            folosite.update(id(s) for s in membri)
    ramase = [s for s in sectiuni if id(s) not in folosite]
    if ramase:
        grupe.append(("altele", "apps", ramase))

    with st.container(key="nav_principal"):
        taburi_ext = st.tabs(
            [_eticheta(icoana, t(f"nav.grupa.{cod}")) for cod, icoana, _ in grupe]
        )

    rezultat = {}
    for tab_ext, (cod, _icoana, membri) in zip(taburi_ext, grupe):
        with tab_ext:
            if len(membri) == 1:
                rezultat[id(membri[0])] = st.container()
            else:
                with st.container(key=f"nav_sub_{cod}"):
                    interioare = st.tabs(
                        [
                            _eticheta(ICONITE.get(s["nume"]), nume_tab(s["nume"]))
                            for s in membri
                        ]
                    )
                for s, tab in zip(membri, interioare):
                    rezultat[id(s)] = tab
    return [rezultat[id(s)] for s in sectiuni]
