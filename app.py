import json
import os

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Încearcă modelele în ordinea asta. Dacă unul e aglomerat sau indisponibil,
# trece la următorul.
MODELE = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
]
MAX_PAGINI = 60


def cheie_api():
    cheie = os.getenv("GOOGLE_API_KEY")
    if cheie:
        return cheie
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return None


def extrage_pagini(fisier):
    doc = pymupdf.open(stream=fisier.read(), filetype="pdf")
    return [{"pagina": i, "text": p.get_text()} for i, p in enumerate(doc, start=1)]


def genereaza_quiz(client, pagini, nr_intrebari, dificultate, limba):
    text = "\n\n".join(f"[Pagina {p['pagina']}]\n{p['text']}" for p in pagini)
    prompt = f"""Ești un profesor care creează teste. Pe baza TEXTULUI de mai jos,
creează {nr_intrebari} întrebări grilă, dificultate {dificultate}, în limba {limba}.

Reguli:
- Folosește DOAR informații din text.
- Fiecare întrebare are exact 4 variante, dintre care una singură corectă.
- Indică pagina de unde provine răspunsul.
- Răspunde DOAR cu JSON valid, fără alt text, în formatul:
[{{"intrebare": "...", "variante": ["A", "B", "C", "D"], "corect": 0, "pagina": 1, "explicatie": "..."}}]
("corect" este indexul variantei corecte, de la 0 la 3)

TEXT:
{text}"""

    ultima_eroare = None
    for model in MODELE:
        try:
            raspuns = client.models.generate_content(model=model, contents=prompt)
            curat = raspuns.text.replace("```json", "").replace("```", "").strip()
            quiz = json.loads(curat)
            return quiz, model
        except Exception as e:
            ultima_eroare = e
            continue  # încearcă următorul model

    raise RuntimeError(
        "Toate modelele sunt indisponibile acum. Încearcă din nou peste "
        f"câteva minute. Ultima eroare: {ultima_eroare}"
    )


st.title("AI Study Buddy")

api_key = cheie_api()
if not api_key:
    st.error("Lipsește cheia API. Verifică fișierul .env sau setările Secrets.")
    st.stop()

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=45000),  # 45 de secunde per încercare
)

fisier = st.file_uploader("Încarcă un PDF", type="pdf")

if fisier:
    pagini = extrage_pagini(fisier)
    st.success(f"PDF încărcat: {len(pagini)} pagini")

    if len(pagini) > MAX_PAGINI:
        st.warning(
            f"PDF-ul are {len(pagini)} pagini. Folosesc doar primele {MAX_PAGINI}."
        )
        pagini = pagini[:MAX_PAGINI]

    col1, col2, col3 = st.columns(3)
    nr = col1.number_input("Număr întrebări", 3, 30, 5)
    dif = col2.selectbox("Dificultate", ["ușoară", "medie", "grea"], index=1)
    limba = col3.selectbox("Limba", ["română", "engleză"])

    if st.button("Generează quiz"):
        with st.spinner("Generez quiz-ul..."):
            try:
                quiz, model_folosit = genereaza_quiz(client, pagini, nr, dif, limba)
                st.session_state["quiz"] = quiz
                st.session_state["model"] = model_folosit
            except Exception as e:
                st.error(f"A apărut o eroare: {e}")

quiz = st.session_state.get("quiz")
if quiz:
    st.header("Quiz")
    st.caption(f"Generat cu: {st.session_state.get('model', '?')}")
    raspunsuri = {}
    for i, q in enumerate(quiz):
        raspunsuri[i] = st.radio(
            f"{i + 1}. {q['intrebare']}",
            q["variante"],
            index=None,
            key=f"q{i}",
        )

    if st.button("Verifică răspunsurile"):
        scor = 0
        for i, q in enumerate(quiz):
            corect = q["variante"][q["corect"]]
            if raspunsuri[i] == corect:
                scor += 1
                st.success(f"{i + 1}. Corect!")
            else:
                st.error(f"{i + 1}. Greșit. Răspuns corect: {corect}")
            st.caption(f"{q['explicatie']} (pagina {q['pagina']})")
        st.subheader(f"Scor: {scor}/{len(quiz)}")
