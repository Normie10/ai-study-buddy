"""AI Study Buddy: fișierul principal (aspectul paginii).

Restul codului e împărțit în fișiere separate:
  config.py        setări și texte
  utile.py         funcții mici
  documente.py     citirea documentelor și alegerea unei părți
  generare.py      modelul AI (prompturi)
  memorie.py       memoria comună (teancurile de întrebări)
  export_html.py   fișierele de descărcat și printat
  examen.py        testul cu cronometru
  taburi.py        secțiunile de bază (Quiz, Examen, SAT, Flashcarduri...)
  sectiuni/        secțiuni noi: fiecare fișier de aici apare singur în aplicație
  baza_date.py     conexiunea la Supabase (cont, materiale salvate, progres)
  autentificare.py ecranul de login / cont nou
"""

import importlib
import os
import sys
from pathlib import Path

import streamlit as st

# Trebuie să fie prima comandă Streamlit din script
st.set_page_config(page_title="AI Study Buddy", layout="centered")

try:
    RADACINA = Path(__file__).resolve().parent
except NameError:  # dacă rulează fără __file__
    RADACINA = Path.cwd()
if str(RADACINA) not in sys.path:
    sys.path.insert(0, str(RADACINA))
DIR_SECTIUNI = RADACINA / "sectiuni"

from dotenv import load_dotenv  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

from autentificare import ecran_autentificare  # noqa: E402
from baza_date import (  # noqa: E402
    NUME_COOKIE,
    delogheaza,
    incearca_restaureaza_sesiune,
    materiale_utilizator,
    salveaza_material,
    sterge_material,
    toate_cookiurile,
    utilizator_curent,
)
from config import (  # noqa: E402
    CSS_APP,
    DESCRIERI_TAB,
    MAX_CARACTERE_LIPIT,
    PLURAL,
    TEXT_FOOTER,
    TEXT_GHID,
)
from documente import (  # noqa: E402
    alege_interval,
    are_text,
    material_din_fisier,
    material_din_text,
)
from taburi import (  # noqa: E402
    Context,
    curata_rezultate,
    tab_carduri,
    tab_examen,
    tab_intreaba,
    tab_quiz,
    tab_rezumat,
    tab_sat,
)
from utile import fmt  # noqa: E402

load_dotenv()

# ------------------------- autentificare -------------------------
# Citim cookie-urile o singură dată, devreme — managerul are nevoie de un
# „rerun” automat ca să le primească efectiv din browser, de-aia facem asta
# chiar la începutul paginii, înainte de orice altceva.
cookies = toate_cookiurile()
incearca_restaureaza_sesiune(cookies)

# Mesaj temporar de depanare — îl scoatem după ce confirmăm că merge
with st.sidebar:
    st.caption(f"[debug] cookie găsit: {'DA' if cookies.get(NUME_COOKIE) else 'NU'}")
    st.caption(f"[debug] logat: {'DA' if utilizator_curent() else 'NU'}")
    st.caption(f"[debug] detaliu: {st.session_state.get('debug_sesiune', '-')}")

# Secțiunile de bază. "ordine" hotărăște poziția (numerele mici apar primele).
SECTIUNI_DE_BAZA = [
    {"nume": "Quiz", "ordine": 10, "cere_material": True,
     "descriere": DESCRIERI_TAB["quiz"], "afiseaza": tab_quiz},
    {"nume": "Examen", "ordine": 20, "cere_material": True,
     "descriere": DESCRIERI_TAB["examen"], "afiseaza": tab_examen},
    {"nume": "SAT", "ordine": 30, "cere_material": False,
     "descriere": "", "afiseaza": tab_sat},
    {"nume": "Flashcarduri", "ordine": 40, "cere_material": True,
     "descriere": DESCRIERI_TAB["carduri"], "afiseaza": tab_carduri},
    {"nume": "Rezumat", "ordine": 50, "cere_material": True,
     "descriere": DESCRIERI_TAB["rezumat"], "afiseaza": tab_rezumat},
    {"nume": "Întreabă", "ordine": 60, "cere_material": True,
     "descriere": DESCRIERI_TAB["intreaba"], "afiseaza": tab_intreaba},
]


def incarca_sectiuni_noi():
    """Încarcă secțiunile din folderul sectiuni/. Fiecare fișier .py de acolo e o
    secțiune nouă și se adaugă singură în aplicație. Un fișier cu probleme nu
    strică restul aplicației: apare doar un avertisment.
    Întoarce (secțiuni, erori)."""
    sectiuni, erori = [], []
    if not DIR_SECTIUNI.is_dir():
        return sectiuni, erori

    init = DIR_SECTIUNI / "__init__.py"
    if not init.exists():
        try:
            init.write_text("", encoding="utf-8")
        except OSError:
            pass
    importlib.invalidate_caches()  # ca să vadă și fișierele create chiar acum

    for fisier in sorted(DIR_SECTIUNI.glob("*.py")):
        if fisier.stem.startswith("_"):
            continue
        try:
            modul = importlib.import_module(f"sectiuni.{fisier.stem}")
            sectiuni.append(
                {
                    "nume": modul.NUME,
                    "ordine": getattr(modul, "ORDINE", 100),
                    "cere_material": getattr(modul, "CERE_MATERIAL", True),
                    "descriere": getattr(modul, "DESCRIERE", ""),
                    "afiseaza": modul.afiseaza,
                    "noua": True,
                }
            )
        except Exception as e:
            erori.append(f"{fisier.name}: {e}")
    return sectiuni, erori


def cheie_api():
    cheie =
