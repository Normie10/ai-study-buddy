import json
import os

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Încearcă modelele în ordinea asta. Dacă unul e aglomerat sau epuizat,
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
    doc = pymupdf.open(stream=fisier.getvalue(), filetype="pdf")
    return [{"pagina": i, "text": p.get_text()} for i, p in enumerate(doc, start=1)]


def text_din_pagini(pagini):
    return "\n\n".join(f"[Pagina {p['pagina']}]\n{p['text']}" for p in pagini)


def cere_json(client, prompt):
    """Trimite promptul la model și întoarce (rezultat_json, model_folosit)."""
    ultima_eroare = None
    for model in MODELE:
        try:
            raspuns = client.models.generate_content(model=model, contents=prompt)
            curat = raspuns.text.replace("```json", "").replace("```", "").strip()
            return json.loads(curat), model
        except Exception as e:
            ultima_eroare = e
            continue  # încearcă următorul model

    raise RuntimeError(
        "Toate modelele sunt indisponibile acum. Încearcă din nou peste "
        f"câteva minute. Ultima eroare: {ultima_eroare}"
    )


def genereaza_quiz(client, pagini, nr_intrebari, dificultate, limba):
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
{text_din_pagini(pagini)}"""
    return cere_json(client, prompt)


def genereaza_carduri(client, pagini, nr_carduri, limba):
    prompt = f"""Ești un profesor care creează flashcarduri pentru memorare.
Pe baza TEXTULUI de mai jos, creează {nr_carduri} flashcarduri în limba {limba}.

Reguli:
- Folosește DOAR informații din text.
- Fața cardului este o întrebare scurtă sau un termen; spatele este un răspuns
  scurt și clar (maximum 2-3 propoziții).
- Fiecare card tratează o singură idee importantă.
- Indică pagina de unde provine informația.
- Răspunde DOAR cu JSON valid, fără alt text, în formatul:
[{{"fata": "...", "spate": "...", "pagina": 1}}]

TEXT:
{text_din_pagini(pagini)}"""
    return cere_json(client, prompt)


def schimba_card(pas, total):
    idx = st.session_state.get("card_idx", 0) + pas
    st.session_state["card_idx"] = max(0, min(total - 1, idx))
    st.session_state["card_arata"] = False


def arata_raspuns():
    st.session_state["card_arata"] = True


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

    limba = st.selectbox("Limba", ["română", "engleză"])

    tab_quiz, tab_carduri = st.tabs(["Quiz", "Flashcarduri"])

    # ---------------- QUIZ ----------------
    with tab_quiz:
        col1, col2 = st.columns(2)
        nr = col1.number_input("Număr întrebări", 3, 30, 5)
        dif = col2.selectbox("Dificultate", ["ușoară", "medie", "grea"], index=1)

        if st.button("Generează quiz"):
            with st.spinner("Generez quiz-ul..."):
                try:
                    quiz, model_folosit = genereaza_quiz(client, pagini, nr, dif, limba)
                    # șterge răspunsurile din quiz-ul anterior
                    for k in list(st.session_state.keys()):
                        if k.startswith("q") and k[1:].isdigit():
                            del st.session_state[k]
                    st.session_state["quiz"] = quiz
                    st.session_state["model_quiz"] = model_folosit
                except Exception as e:
                    st.error(f"A apărut o eroare: {e}")

        quiz = st.session_state.get("quiz")
        if quiz:
            st.header("Quiz")
            st.caption(f"Generat cu: {st.session_state.get('model_quiz', '?')}")
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

    # ------------- FLASHCARDURI -------------
    with tab_carduri:
        nr_carduri = st.number_input("Număr flashcarduri", 5, 40, 10)

        if st.button("Generează flashcarduri"):
            with st.spinner("Generez flashcardurile..."):
                try:
                    carduri, model_folosit = genereaza_carduri(
                        client, pagini, nr_carduri, limba
                    )
                    st.session_state["carduri"] = carduri
                    st.session_state["model_carduri"] = model_folosit
                    st.session_state["card_idx"] = 0
                    st.session_state["card_arata"] = False
                except Exception as e:
                    st.error(f"A apărut o eroare: {e}")

        carduri = st.session_state.get("carduri")
        if carduri:
            total = len(carduri)
            idx = min(st.session_state.get("card_idx", 0), total - 1)
            card = carduri[idx]

            st.caption(
                f"Card {idx + 1} din {total} · "
                f"Generat cu: {st.session_state.get('model_carduri', '?')}"
            )
            with st.container(border=True):
                st.markdown("**Întrebare**")
                st.subheader(card.get("fata", ""))
                if st.session_state.get("card_arata"):
                    st.divider()
                    st.markdown("**Răspuns**")
                    st.write(card.get("spate", ""))
                    st.caption(f"Pagina {card.get('pagina', '?')}")

            c1, c2, c3 = st.columns(3)
            c1.button(
                "← Înapoi",
                on_click=schimba_card,
                args=(-1, total),
                disabled=(idx == 0),
            )
            c2.button("Arată răspunsul", on_click=arata_raspuns)
            c3.button(
                "Următorul →",
                on_click=schimba_card,
                args=(1, total),
                disabled=(idx == total - 1),
            )
