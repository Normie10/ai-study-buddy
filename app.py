"""AI Study Buddy: fișierul principal (aspectul paginii).

Restul codului e împărțit în fișiere separate:
  config.py          setări, texte și stilul aplicației (CSS)
  limbi.py           traducerea interfeței (română / engleză)
  navigare.py        taburile grupate (Exersează, Învață, Progres)
  stil_ui.py         stil în plus: taburi mici, răspunsuri ca niște carduri
  stil_notificari.py notificările fixe (rotița de încărcare, avertismentul)
  obiectiv_zilnic.py obiectivul zilnic și seria de zile
  abonamente.py      pagina de abonamente (prototip)
  explicatii.py      explicațiile pentru răspunsurile greșite
  utile.py           funcții mici
  documente.py       citirea documentelor și alegerea unei părți
  generare.py        modelul AI (prompturi)
  memorie.py         memoria comună (teancurile de întrebări)
  export_html.py     fișierele de descărcat și printat
  examen.py          testul cu cronometru
  taburi.py          secțiunile de bază (Quiz, Examen, SAT, Flashcarduri...)
  sectiuni/          secțiuni noi: fiecare fișier de aici apare singur în aplicație
  baza_date.py       conexiunea la Supabase (cont, materiale salvate, progres)
  autentificare.py   ecranul de login / cont nou / vizitator / resetare parolă
"""

import html
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

from abonamente import (  # noqa: E402
    afiseaza_pagina_abonamente,
    antet_profil,
    butoane_vizitator,
)

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
from config import CSS_APP, MAX_CARACTERE_LIPIT  # noqa: E402
from documente import (  # noqa: E402
    alege_interval,
    are_text,
    material_din_fisier,
    material_din_text,
)
from limbi import (  # noqa: E402
    descriere_sectiune,
    nume_tab,
    selector_limba,
    t,
    unitate_ui,
)
from navigare import NUME_CUNOSCUTE, taburi_grupate  # noqa: E402
from obiectiv_zilnic import afiseaza_obiectiv  # noqa: E402
from stil_notificari import CSS_NOTIFICARI  # noqa: E402
from stil_corecturi import CSS_UI  # noqa: E402
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

# Stilul se încarcă primul, ca să se aplice și ecranelor de login / resetare.
st.markdown(CSS_APP, unsafe_allow_html=True)
st.markdown(CSS_NOTIFICARI, unsafe_allow_html=True)
st.markdown(CSS_UI, unsafe_allow_html=True)

# Valorile interne ale alegerii sursei (nu se traduc: logica se bazează pe ele)
SURSA_FISIER = "Încarcă un fișier"
SURSA_TEXT = "Lipește text"

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

# Secțiunile de bază. "ordine" hotărăște poziția în lista internă. Numele și
# descrierile afișate vin din limbi.py, după numele secțiunii.
SECTIUNI_DE_BAZA = [
    {"nume": "Quiz", "ordine": 10, "cere_material": True,
     "descriere": "", "afiseaza": tab_quiz},
    {"nume": "Examen", "ordine": 20, "cere_material": True,
     "descriere": "", "afiseaza": tab_examen},
    {"nume": "SAT", "ordine": 30, "cere_material": False,
     "descriere": "", "afiseaza": tab_sat},
    {"nume": "Flashcarduri", "ordine": 40, "cere_material": True,
     "descriere": "", "afiseaza": tab_carduri},
    {"nume": "Rezumat", "ordine": 50, "cere_material": True,
     "descriere": "", "afiseaza": tab_rezumat},
    {"nume": "Întreabă", "ordine": 60, "cere_material": True,
     "descriere": "", "afiseaza": tab_intreaba},
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


def inchide_avertisment_salvare():
    """Ascunde mesajul galben despre scorul care nu s-a putut salva."""
    st.session_state.pop("eroare_salvare", None)


def incarca_material_salvat(continut):
    """Pune conținutul unui material salvat în caseta de text, ca să fie
    folosit ca și cum tocmai l-ai lipit."""
    st.session_state["sursa_material"] = SURSA_TEXT
    st.session_state["text_lipit"] = continut
    st.session_state["caseta_text"] = continut


# ------------------------- piese de aspect -------------------------
def hero_html():
    """Antetul aplicației. Totul pe un singur rând, fără linii goale, altfel
    Markdown îl strică."""
    return (
        '<div class="hero"><div class="hero-marca"></div><div>'
        f'<div class="hero-titlu">{html.escape(t("hero.titlu"))}</div>'
        f'<div class="hero-sub">{html.escape(t("hero.sub"))}</div>'
        "</div></div>"
    )


def pas_titlu(numar, text):
    """Antetul unui pas: un cerc roșu cu numărul și titlul alături."""
    st.markdown(
        f'<div class="pas"><span class="pas-nr">{numar}</span>'
        f'<span class="pas-titlu">{html.escape(text)}</span></div>',
        unsafe_allow_html=True,
    )


def stare_goala(descriere):
    """Ce se vede într-o secțiune când nu e ales încă niciun material."""
    st.markdown(
        '<div class="gol">'
        f'<div class="gol-titlu">{html.escape(t("gol.titlu"))}</div>'
        f'<div class="gol-text">{html.escape(descriere)}</div>'
        f'<div class="gol-indiciu">{html.escape(t("gol.indiciu"))}</div>'
        "</div>",
        unsafe_allow_html=True,
    )


def _rezumat_progres():
    """Două numere rapide: total încercări și scor mediu. Pentru popover-ul
    de profil — statisticile complete sunt în secțiunea Progresul meu."""
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
    materiale salvate, limba, delogare."""
    if utilizator_curent() is not None:
        antet_profil(utilizator_curent().email)

        rezumat = _rezumat_progres()
        if rezumat:
            total, medie = rezumat
            c1, c2 = st.columns(2)
            c1.metric(t("profil.incercari"), total)
            c2.metric(t("profil.scor_mediu"), f"{medie}%")
        else:
            st.caption(t("profil.fara_rezultate"))

        st.divider()
        st.markdown(f"**{t('profil.materiale')}**")
        try:
            materiale = materiale_utilizator()
        except Exception as e_mat:
            st.warning(t("profil.materiale.eroare", e=e_mat))
            materiale = []
        if not materiale:
            st.caption(t("profil.materiale.gol"))
        else:
            for m in materiale:
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(m["nume"])
                if c2.button(t("profil.incarca"), key=f"mat_inc_{m['id']}"):
                    incarca_material_salvat(m["continut"])
                    st.rerun()
                if c3.button(t("profil.sterge"), key=f"mat_st_{m['id']}"):
                    try:
                        sterge_material(m["id"])
                        st.rerun()
                    except Exception as e_st:
                        st.error(t("profil.sterge.eroare", e=e_st))

        st.divider()
        selector_limba()
        if st.button(
            t("profil.delogare"), key="profil_delogare", use_container_width=True
        ):
            delogheaza()
            st.rerun()

    else:
        st.caption(t("profil.vizitator"))
        selector_limba()
        if butoane_vizitator():
            iese_din_mod_vizitator()
            st.rerun()


def pasul_material():
    """Pasul 1: limba și materialul. Întoarce (limba, material, părțile alese, hash)."""
    mat = None
    selectate = None
    hash_material = None

    with st.container(border=True):
        pas_titlu(1, t("pas.1"))

        c_limba, c_sursa = st.columns([1, 1.4])
        with c_limba:
            limba = st.selectbox(
                t("material.limba"),
                ["română", "engleză"],
                format_func=lambda v: (
                    t("limba.romana") if v == "română" else t("limba.engleza")
                ),
                help=t("material.limba.help"),
            )
        with c_sursa:
            sursa = st.radio(
                t("material.sursa"),
                [SURSA_FISIER, SURSA_TEXT],
                format_func=lambda v: (
                    t("sursa.fisier") if v == SURSA_FISIER else t("sursa.text")
                ),
                horizontal=True,
                key="sursa_material",
                help=t("material.sursa.help"),
            )

        if sursa == SURSA_FISIER:
            fisier = st.file_uploader(
                t("material.fisier"),
                type=["pdf", "docx", "txt", "md"],
            )
            if fisier:
                try:
                    mat = material_din_fisier(fisier)
                except Exception as e_fis:
                    st.error(t("material.fisier.eroare", e=e_fis))
        else:
            with st.form("form_text"):
                text_nou = st.text_area(
                    t("material.text.eticheta", max=fmt(MAX_CARACTERE_LIPIT)),
                    height=250,
                    max_chars=MAX_CARACTERE_LIPIT,
                    key="caseta_text",
                )
                trimis_text = st.form_submit_button(t("material.text.buton"))
            if trimis_text:
                st.session_state["text_lipit"] = text_nou

            text_curent = st.session_state.get("text_lipit", "")
            if text_curent.strip():
                mat = material_din_text(text_curent)
                b1, b2, _liber = st.columns([1, 1.7, 2.3])
                b1.button(t("material.text.sterge"), on_click=sterge_textul)
                if not este_vizitator():
                    if b2.button(t("material.text.salveaza")):
                        try:
                            salveaza_material(mat["nume"], text_curent)
                            st.success(t("material.text.salvat"))
                        except Exception as e_salv:
                            st.error(t("material.text.eroare_salvare", e=e_salv))

        if mat is not None and not are_text(mat):
            st.error(t("material.fara_text"))
            mat = None

        if mat is not None:
            n_unitati = len(mat["unitati"])
            total_caractere = sum(len(u["text"]) for u in mat["unitati"])
            nume_afisat = (
                t("material.text_lipit") if mat["nume"] == "Text lipit" else mat["nume"]
            )
            st.success(
                t(
                    "material.gata",
                    nume=nume_afisat,
                    n=n_unitati,
                    unitate=unitate_ui(mat["eticheta"]),
                    car=fmt(total_caractere),
                )
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
# pagina de abonamente: înlocuiește tot restul paginii (și meniul de profil,
# ca să nu rămână deschis peste ea)
if st.session_state.get("pagina_abonamente"):
    afiseaza_pagina_abonamente()
    st.stop()

with st.container(key="profil_fixat"):
    if utilizator_curent() is not None:
        eticheta_profil = utilizator_curent().email.split("@")[0]
    else:
        eticheta_profil = t("profil.vizitator.eticheta")
    with st.popover(eticheta_profil, icon=":material/account_circle:"):
        panou_profil()

st.markdown(hero_html(), unsafe_allow_html=True)

# containerele din secțiunea „Progresul meu” unde se desenează obiectivul zilnic
# (se completează la finalul paginii)
zone_obiectiv = []

# loc rezervat pentru avertismentul de salvare: îl completăm la finalul paginii,
# după ce toate secțiunile au rulat (o salvare poate eșua oriunde în pagină).
# Plutește pe ecran, vezi stil_notificari.py
zona_avertisment = st.container(key="avert_salvare")

# loc rezervat pentru ghid: îl completăm după ce știm ce secțiuni există
zona_intro = st.container()

api_key = cheie_api()
if not api_key:
    st.error(t("eroare.cheie_api"))
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


# obiectivul zilnic stă în secțiunea „Progresul meu”: îi punem un loc rezervat
# la început, pe care îl completăm la finalul paginii
def _cu_loc_pentru_obiectiv(functie):
    def invelita(ctx):
        zone_obiectiv.append(st.container())
        functie(ctx)

    return invelita


for s in sectiuni_noi:
    if "progres" in s["nume"].lower():
        s["afiseaza"] = _cu_loc_pentru_obiectiv(s["afiseaza"])
        break

# ghidul: închis implicit (pagina rămâne curată); se deschide cu un click
with zona_intro:
    with st.expander(t("ghid.titlu"), expanded=False):
        st.markdown(t("ghid.text"))
        necunoscute = [
            s for s in sectiuni_noi
            if s["nume"] not in NUME_CUNOSCUTE and s["descriere"]
        ]
        if necunoscute:
            st.markdown(
                f"**{t('ghid.adaugate')}**\n\n"
                + "\n".join(
                    f"- **{nume_tab(s['nume'])}:** "
                    f"{descriere_sectiune(s['nume'], s['descriere'])}"
                    for s in necunoscute
                )
            )

# ---------------- pasul 2: ce vrei să faci ----------------
pas_titlu(2, t("pas.2"))

for eroare in erori_sectiuni:
    st.warning(t("eroare.sectiune_noua", eroare=eroare))

taburi_ui = taburi_grupate(sectiuni)
for tab, s in zip(taburi_ui, sectiuni):
    with tab:
        if s["cere_material"] and not are_material:
            stare_goala(descriere_sectiune(s["nume"], s["descriere"]))
        elif s.get("noua"):
            try:
                s["afiseaza"](ctx)
            except Exception as e_sectiune:
                st.error(
                    t("eroare.sectiune", nume=nume_tab(s["nume"]), e=e_sectiune)
                )
        else:
            s["afiseaza"](ctx)

# obiectivul zilnic: se desenează abia acum, ca să includă și ce s-a terminat
# chiar în această rulare (un quiz predat, un test încheiat)
for zona_ob in zone_obiectiv:
    afiseaza_obiectiv(zona_ob)

# avertisment: dacă un scor nu s-a putut salva pe cont, apare ca notificare fixă
motiv_salvare = st.session_state.get("eroare_salvare")
if motiv_salvare:
    with zona_avertisment:
        st.warning(t("avert.salvare"))
        st.caption(t("avert.detalii", motiv=motiv_salvare))
        st.button(
            t("avert.inchide"),
            on_click=inchide_avertisment_salvare,
            key="inchide_avert_salvare",
        )

st.markdown(
    f'<div class="subsol">{html.escape(t("footer"))}</div>',
    unsafe_allow_html=True,
)
