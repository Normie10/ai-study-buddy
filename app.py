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
  autentificare.py ecranul de login / cont nou / vizitator / resetare parolă
"""

import importlib
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs

import streamlit as st
from streamlit_javascript import st_javascript

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

from autentificare import ecran_autentificare, ecran_parola_noua  # noqa: E402
from baza_date import (  # noqa: E402
    delogheaza,
    este_vizitator,
    iese_din_mod_vizitator,
    incearca_restaureaza_sesiune,
    materiale_utilizator,
    progres_utilizator,
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

# ------------------------- link de resetare a parolei -------------------------
# Supabase trimite link-ul de resetare cu token-urile ascunse după # (o bucată
# din adresă pe care doar browser-ul o vede). Streamlit nu poate schimba
# adresa din bara browser-ului, dar POATE citi ce scrie acolo — exact asta
# facem, fără să mișcăm nimic din adresă.
if "in_recuperare_parola" not in st.session_state:
    url_hash = st_javascript("window.parent.location.hash")
    if (
        isinstance(url_hash, str)
        and "access_token" in url_hash
        and "type=recovery" in url_hash
    ):
        params = parse_qs(url_hash.lstrip("#"))
        access_token = params.get("access_token", [None])[0]
        refresh_token = params.get("refresh_token", [None])[0]
        if access_token:
            st.session_state["in_recuperare_parola"] = True
            st.session_state["recuperare_access_token"] = access_token
            st.session_state["recuperare_refresh_token"] = refresh_token or ""

if st.session_state.get("in_recuperare_parola"):
    ecran_parola_noua(
        st.session_state.get("recuperare_access_token"),
        st.session_state.get("recuperare_refresh_token", ""),
    )
    st.stop()

# ------------------------- autentificare -------------------------
cookies = toate_cookiurile()
incearca_restaureaza_sesiune(cookies)

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
    cheie = os.getenv("GOOGLE_API_KEY")
    if cheie:
        return cheie
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return None


def sterge_textul():
    st.session_state["text_lipit"] = ""
    st.session_state["caseta_text"] = ""


def incarca_material_salvat(continut):
    """Pune conținutul unui material salvat în caseta de text, ca să fie
    folosit ca și cum tocmai l-ai lipit."""
    st.session_state["sursa_material"] = "Lipește text"
    st.session_state["text_lipit"] = continut
    st.session_state["caseta_text"] = continut


def _rezumat_progres():
    """Două numere rapide: total încercări și scor mediu. Pentru popover-ul
    de profil — statisticile complete sunt în tab-ul Progresul meu."""
    try:
        istoric = progres_utilizator()
    except Exception:
        return None
    if not istoric:
        return None
    total = len(istoric)
    procente = [100 * r["scor"] / r["total"] for r in istoric if r["total"]]
    medie = round(sum(procente) / len(procente)) if procente else 0
    return total, medie


def panou_profil():
    """Conținutul butonului de profil: cont/vizitator, progres rapid,
    materiale salvate, delogare."""
    if utilizator_curent() is not None:
        st.write(f"**{utilizator_curent().email}**")

        rezumat = _rezumat_progres()
        if rezumat:
            total, medie = rezumat
            c1, c2 = st.columns(2)
            c1.metric("Încercări", total)
            c2.metric("Scor mediu", f"{medie}%")
        else:
            st.caption("Niciun rezultat salvat încă.")

        st.divider()
        st.markdown("**Materialele mele**")
        try:
            materiale = materiale_utilizator()
        except Exception as e_mat:
            st.warning(f"Nu am putut încărca materialele: {e_mat}")
            materiale = []
        if not materiale:
            st.caption("Niciun material salvat încă.")
        else:
            for m in materiale:
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(m["nume"])
                if c2.button("Încarcă", key=f"mat_inc_{m['id']}"):
                    incarca_material_salvat(m["continut"])
                    st.rerun()
                if c3.button("Șterge", key=f"mat_st_{m['id']}"):
                    try:
                        sterge_material(m["id"])
                        st.rerun()
                    except Exception as e_st:
                        st.error(f"Nu am putut șterge: {e_st}")

        st.divider()
        if st.button("Delogare", key="profil_delogare", use_container_width=True):
            delogheaza()
            st.rerun()

    else:
        st.caption(
            "Ești vizitator — materialele și progresul nu se salvează."
        )
        if st.button("Creează cont", key="profil_creeaza_cont", use_container_width=True):
            iese_din_mod_vizitator()
            st.rerun()


def pasul_material():
    """Pasul 1: limba și materialul. Întoarce (limba, material, părțile alese, hash)."""
    mat = None
    selectate = None
    hash_material = None

    with st.container(border=True):
        st.subheader("1. Alege materialul")

        limba = st.selectbox(
            "Limba întrebărilor și a explicațiilor",
            ["română", "engleză"],
            help="La SAT, întrebările rămân în engleză; explicațiile urmează această limbă.",
        )

        sursa = st.radio(
            "De unde iei materialul? (nu e nevoie pentru SAT)",
            ["Încarcă un fișier", "Lipește text"],
            horizontal=True,
            key="sursa_material",
        )

        if sursa == "Încarcă un fișier":
            fisier = st.file_uploader(
                "PDF, Word (.docx) sau text (.txt, .md)",
                type=["pdf", "docx", "txt", "md"],
            )
            if fisier:
                try:
                    mat = material_din_fisier(fisier)
                except Exception as e_fis:
                    st.error(f"Nu am putut citi fișierul: {e_fis}")
        else:
            with st.form("form_text"):
                text_nou = st.text_area(
                    f"Lipește aici textul (Ctrl+V). Maximum {fmt(MAX_CARACTERE_LIPIT)} de caractere.",
                    height=250,
                    max_chars=MAX_CARACTERE_LIPIT,
                    key="caseta_text",
                )
                trimis_text = st.form_submit_button("Folosește acest text")
            if trimis_text:
                st.session_state["text_lipit"] = text_nou

            text_curent = st.session_state.get("text_lipit", "")
            if text_curent.strip():
                mat = material_din_text(text_curent)
                b1, b2 = st.columns(2)
                b1.button("Șterge textul", on_click=sterge_textul)
                if not este_vizitator():
                    if b2.button("Salvează acest material pe cont"):
                        try:
                            salveaza_material(mat["nume"], text_curent)
                            st.success("Material salvat pe cont.")
                        except Exception as e_salv:
                            st.error(f"Nu am putut salva: {e_salv}")

        if mat is not None and not are_text(mat):
            st.error(
                "Nu am găsit text în document. Dacă e un PDF scanat (poze cu text), "
                "momentan nu pot citi text din imagini."
            )
            mat = None

        if mat is not None:
            n_unitati = len(mat["unitati"])
            total_caractere = sum(len(u["text"]) for u in mat["unitati"])
            st.success(
                f"{mat['nume']}: {n_unitati} {PLURAL[mat['eticheta']]}, "
                f"aproximativ {fmt(total_caractere)} de caractere"
            )
            selectate, hash_material = alege_interval(mat)

            if st.session_state.get("hash_material") != hash_material:
                curata_rezultate()
                st.session_state["hash_material"] = hash_material

    return limba, mat, selectate, hash_material


if utilizator_curent() is None and not este_vizitator():
    ecran_autentificare()
    st.stop()

# ------------------------- pagina -------------------------
st.markdown(CSS_APP, unsafe_allow_html=True)

with st.container(key="profil_fixat"):
    if utilizator_curent() is not None:
        eticheta_profil = utilizator_curent().email.split("@")[0]
    else:
        eticheta_profil = "Vizitator"
    with st.popover(eticheta_profil):
        panou_profil()

st.title("AI Study Buddy")
  
st.caption(
    "Transformă materialele tale în quiz-uri, teste cu cronometru, flashcarduri "
    "și rezumate."
)

# loc rezervat pentru ghid: îl completăm după ce știm dacă există un material
zona_intro = st.container()

api_key = cheie_api()
if not api_key:
    st.error("Lipsește cheia API. Verifică fișierul .env sau setările Secrets.")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=90000),  # 90 de secunde per încercare
)

limba, mat, selectate, hash_material = pasul_material()
ctx = Context(
    client=client,
    limba=limba,
    mat=mat,
    selectate=selectate,
    hash_material=hash_material,
)
are_material = mat is not None and selectate is not None

sectiuni_noi, erori_sectiuni = incarca_sectiuni_noi()
sectiuni = sorted(SECTIUNI_DE_BAZA + sectiuni_noi, key=lambda s: s["ordine"])

# ghidul: deschis pentru cine intră prima oară, închis după ce există un material
with zona_intro:
    with st.expander("Cum funcționează?", expanded=(mat is None)):
        st.markdown(TEXT_GHID)
        descrise = [s for s in sectiuni_noi if s["descriere"]]
        if descrise:
            st.markdown(
                "**Secțiuni adăugate**\n\n"
                + "\n".join(f"- **{s['nume']}:** {s['descriere']}" for s in descrise)
            )

# ---------------- pasul 2: ce vrei să faci ----------------
st.subheader("2. Alege ce vrei să faci")

for eroare in erori_sectiuni:
    st.warning(
        f"O secțiune nouă nu s-a putut încărca ({eroare}). "
        "Restul aplicației merge normal."
    )

taburi_ui = st.tabs([s["nume"] for s in sectiuni])
for tab, s in zip(taburi_ui, sectiuni):
    with tab:
        if s["cere_material"] and not are_material:
            st.info(
                f"{s['descriere']}\n\n"
                "Încarcă un document (sau lipește text) la pasul 1 ca să începi."
            )
        elif s.get("noua"):
            try:
                s["afiseaza"](ctx)
            except Exception as e_sectiune:
                st.error(f"Secțiunea „{s['nume']}” a dat o eroare: {e_sectiune}")
        else:
            s["afiseaza"](ctx)

st.divider()
st.caption(TEXT_FOOTER)
