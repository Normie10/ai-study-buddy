import json
import os
import time

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.8-flash"
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

    raspuns = None
    for incercare in range(4):
        try:
            raspuns = client.models.generate_content(model=MODEL, contents=prompt)
            break
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and incercare < 3:
                time.sleep(5 * (incercare + 1))  # așteaptă 5, 10, 15 secunde
            else:
                raise

    curat = raspuns.text.replace("```json", "").replace("```", "").strip()
    return json.loads(curat)


st.title("AI Study Buddy")

api_key = cheie_api()
if not api_key:
    st.error("Lipsește cheia API. Verifică fișierul .env sau setările Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

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
                st.session_state["quiz"] = genereaza_quiz(
                    client, pagini, nr, dif, limba
                )
            except Exception as e:
                st.error(f"A apărut o eroare: {e}")

quiz = st.session_state.get("quiz")
if quiz:
    st.header("Quiz")
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