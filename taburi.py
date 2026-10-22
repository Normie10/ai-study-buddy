"""Câte o funcție pentru fiecare secțiune a aplicației: Quiz, Examen, SAT,
Flashcarduri, Rezumat, Întreabă."""

import random
from dataclasses import dataclass

import streamlit as st

from baza_date import salveaza_progres
from config import (
    DESCRIERI_TAB,
    DISCLAIMER_SAT,
    MAX_INTREBARI_SAT,
    MAX_INTREBARI_SESIUNE,
    MAX_LUNGIME_INTREBARE,
    MINUTE_SAT,
    NIVELE_REZUMAT,
    NIVELE_SAT,
    SECTIUNI_SAT,
    TIP_AF,
    TIP_GRILA,
    TIPURI_INTREBARI,
)
from documente import alege_fragmente, descrie_surse
from examen import afiseaza_examen
from export_html import html_carduri, html_quiz
from generare import (
    genereaza_rezumat,
    genereaza_teanc_af,
    genereaza_teanc_carduri,
    genereaza_teanc_quiz,
    genereaza_teanc_sat,
    raspunde_intrebare,
)
from memorie import (
    amesteca_variante,
    citeste,
    preia_din_teanc,
    preia_pentru_examen,
    salveaza,
)
from utile import norm, text_intrebare


@dataclass
class Context:
    """Ce știu secțiunile despre materialul ales."""

    client: object
    limba: str
    mat: dict = None
    selectate: list = None
    hash_material: str = None

    @property
    def eticheta(self):
        return self.mat["eticheta"]


def curata_rezultate():
    """Șterge rezultatele afișate (quiz, carduri, rezumat) când se schimbă materialul."""
    for k in (
        "quiz",
        "quiz_predat",
        "info_quiz",
        "carduri",
        "info_carduri",
        "studiu",
        "rezumat",
        "info_rezumat",
    ):
        st.session_state.pop(k, None)
    for k in list(st.session_state.keys()):
        if k.startswith("q") and k[1:].isdigit():
            del st.session_state[k]


def info_fara_material(cheie_tab):
    """Ce se vede într-o secțiune când nu e încărcat niciun document."""
    st.info(
        f"{DESCRIERI_TAB[cheie_tab]}\n\n"
        "Încarcă un document (sau lipește text) la pasul 1 ca să începi."
    )


def alege_intrebari(ctx, tip, nr, dif, pentru_examen=False):
    """Alege întrebările pentru quiz sau examen, în funcție de tipul cerut
    (grilă, Adevărat/Fals sau amestecat). Întoarce (întrebări, model, notă)."""
    preia = preia_pentru_examen if pentru_examen else preia_din_teanc

    def grila(n):
        return preia(
            ("quiz", ctx.hash_material, dif, ctx.limba),
            n,
            "intrebare",
            lambda: genereaza_teanc_quiz(
                ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
            ),
        )

    def adevarat_fals(n):
        return preia(
            ("af", ctx.hash_material, dif, ctx.limba),
            n,
            "intrebare",
            lambda: genereaza_teanc_af(
                ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
            ),
        )

    if tip == TIP_GRILA:
        return grila(nr)
    if tip == TIP_AF:
        return adevarat_fals(nr)

    # amestecat: jumătate grilă, jumătate Adevărat/Fals, în ordine amestecată
    n_af = nr // 2
    n_grila = nr - n_af
    el1, model1, nota1 = grila(n_grila)
    el2, model2, nota2 = adevarat_fals(n_af)
    elemente = el1 + el2
    random.shuffle(elemente)
    model = model1 if model1 == model2 else f"{model1} + {model2}"
    nota = nota1 if nota1 == nota2 else f"{nota1}; {nota2}"
    return elemente, model, nota


def reface_quiz_doar_greseli(gresite):
    """Pornește un quiz nou, doar cu întrebările greșite la ultima predare."""
    for k in list(st.session_state.keys()):
        if k.startswith("q") and k[1:].isdigit():
            del st.session_state[k]
    st.session_state["quiz"] = list(gresite)
    st.session_state.pop("quiz_predat", None)
    st.session_state["info_quiz"] = "Recapitulare greșeli"


# ---------------- QUIZ ----------------
def tab_quiz(ctx):
    st.caption(DESCRIERI_TAB["quiz"])
    tip = st.selectbox("Tip de întrebări", TIPURI_INTREBARI, key="quiz_tip")
    col1, col2 = st.columns(2)
    nr = col1.number_input("Număr întrebări", 3, 20, 5)
    dif = col2.selectbox("Dificultate", ["ușoară", "medie", "grea"], index=1)

    if st.button("Generează quiz"):
        with st.spinner("Pregătesc quiz-ul..."):
            try:
                elemente, model_folosit, nota = alege_intrebari(ctx, tip, nr, dif)
                quiz = [amesteca_variante(q) for q in elemente]
                # șterge răspunsurile din quiz-ul anterior
                for k in list(st.session_state.keys()):
                    if k.startswith("q") and k[1:].isdigit():
                        del st.session_state[k]
                st.session_state["quiz"] = quiz
                st.session_state.pop("quiz_predat", None)  # quiz nou, nepredat
                st.session_state["info_quiz"] = f"{model_folosit} · {nota}"
            except Exception as e_quiz:
                st.error(f"A apărut o eroare: {e_quiz}")

    quiz = st.session_state.get("quiz")
    if quiz:
        st.subheader("Quiz")
        st.caption(f"Model: {st.session_state.get('info_quiz', '?')}")
        st.download_button(
            "Descarcă quiz-ul pentru printat (.html)",
            data=html_quiz(quiz),
            file_name="quiz.html",
            mime="text/html",
            on_click="ignore",
            key="dl_quiz",
        )

        predat = st.session_state.get("quiz_predat")
        raspunsuri = {}
        for i, q in enumerate(quiz):
            raspunsuri[i] = st.radio(
                f"{i + 1}. {text_intrebare(q)}",
                q["variante"],
                index=None,
                key=f"q{i}",
                disabled=predat is not None,  # după predare, răspunsurile se blochează
            )

        if predat is None:
            if st.button("Predă răspunsurile", key="quiz_preda"):
                scor = sum(
                    1
                    for i, q in enumerate(quiz)
                    if raspunsuri[i] == q["variante"][q["corect"]]
                )
                # se salvează o singură dată: prima predare e cea finală
                salveaza_progres("quiz", scor, len(quiz))
                st.session_state["quiz_predat"] = {
                    "raspunsuri": dict(raspunsuri),
                    "scor": scor,
                }
                st.rerun()  # redesenează cu răspunsurile blocate
        else:
            scor = predat["scor"]
            gresite = []
            for i, q in enumerate(quiz):
                corect = q["variante"][q["corect"]]
                ales = predat["raspunsuri"].get(i)
                if ales == corect:
                    st.success(f"{i + 1}. Corect!")
                else:
                    st.error(f"{i + 1}. Greșit. Răspuns corect: {corect}")
                    gresite.append(q)
                st.caption(
                    f"{q['explicatie']} ({q.get('unitate', 'pagina')} {q['pagina']})"
                )
            st.subheader(f"Scor: {scor}/{len(quiz)}")
            if gresite:
                st.button(
                    f"Recapitulează doar greșelile ({len(gresite)})",
                    on_click=reface_quiz_doar_greseli,
                    args=(gresite,),
                    key="quiz_recap_greseli",
                    type="primary",
                )
            st.caption(
                "Răspunsurile au fost predate. Pentru o nouă încercare, "
                "generează un quiz nou."
            )


# ---------------- EXAMEN (din document) ----------------
def tab_examen(ctx):
    def formular_examen():
        st.caption(DESCRIERI_TAB["examen"])
        tip_ex = st.selectbox("Tip de întrebări", TIPURI_INTREBARI, key="ex_tip")
        c1, c2, c3 = st.columns(3)
        nr_ex = c1.number_input("Număr întrebări", 5, 30, 10, key="ex_nr")
        dif_ex = c2.selectbox(
            "Dificultate", ["ușoară", "medie", "grea"], index=1, key="ex_dif"
        )
        minute = c3.number_input("Timp (minute)", 1, 90, 15, key="ex_min")

        if st.button("Începe examenul", key="ex_start"):
            with st.spinner("Pregătesc examenul..."):
                try:
                    elemente, model_folosit, nota = alege_intrebari(
                        ctx, tip_ex, nr_ex, dif_ex, pentru_examen=True
                    )
                    return {
                        "sursa": "document",
                        "titlu": "Rezultate examen",
                        "intrebari": [amesteca_variante(q) for q in elemente],
                        "cerute": nr_ex,
                        "durata": int(minute * 60),
                        "info": f"{model_folosit} · {nota}",
                    }
                except Exception as e_ex:
                    st.error(f"A apărut o eroare: {e_ex}")
        return None

    afiseaza_examen("examen", ctx.hash_material, formular_examen)


# ---------------- SAT (nu are nevoie de document) ----------------
def tab_sat(ctx):
    def formular_sat():
        st.write(
            "Întrebări în stilul SAT-ului digital, **fără legătură cu documentul** "
            "încărcat. Întrebările sunt în engleză; explicațiile urmează limba "
            "aleasă mai sus."
        )
        st.info(DISCLAIMER_SAT)

        c1, c2 = st.columns(2)
        sectiune = c1.selectbox("Secțiune", list(SECTIUNI_SAT.keys()), key="sat_sectiune")
        dif_sat = c2.selectbox(
            "Dificultate", list(NIVELE_SAT.keys()), index=1, key="sat_dif"
        )
        tip = SECTIUNI_SAT[sectiune]

        c3, c4 = st.columns(2)
        nr_sat = c3.number_input(
            "Număr întrebări", 5, MAX_INTREBARI_SAT, 10, key="sat_nr"
        )
        minute = c4.number_input(
            "Timp (minute)", 1, 90, MINUTE_SAT[tip], key=f"sat_min_{tip}"
        )
        st.caption(
            "Timpul implicit e calculat după ritmul de pe SAT-ul digital "
            "(în jur de 71 de secunde pe întrebare la Reading and Writing și 95 la "
            "Math). Verifică formatul actual pe collegeboard.org."
        )

        if st.button("Începe testul SAT", key="sat_start"):
            with st.spinner("Pregătesc întrebările..."):
                try:
                    n = max(10, nr_sat)
                    elemente, model_folosit, nota = preia_din_teanc(
                        ("sat", tip, dif_sat, ctx.limba),
                        nr_sat,
                        "dedup",
                        lambda: genereaza_teanc_sat(
                            ctx.client, tip, dif_sat, ctx.limba, n
                        ),
                    )
                    return {
                        "sursa": "sat",
                        "titlu": f"Rezultate SAT - {sectiune}",
                        "intrebari": [amesteca_variante(q) for q in elemente],
                        "cerute": nr_sat,
                        "durata": int(minute * 60),
                        "info": f"{model_folosit} · {nota}",
                    }
                except Exception as e_sat:
                    st.error(f"A apărut o eroare: {e_sat}")
        return None

    afiseaza_examen("sat", "sat", formular_sat)


# ------------- FLASHCARDURI (cu repetare) -------------
def porneste_studiu(n, ids=None):
    """Începe o sesiune de studiu. `ids` = indicii cardurilor de studiat
    (implicit toate, de la 0 la n-1). Cardurile se amestecă."""
    ids = list(range(n)) if ids is None else list(ids)
    random.shuffle(ids)
    st.session_state["studiu"] = {
        "ids": list(ids),  # cardurile acestei sesiuni
        "coada": list(ids),  # ce a mai rămas de învățat (fiecare card o singură dată)
        "gresite": {},  # card -> de câte ori am greșit
        "incercari": 0,
        "arata": False,
    }


def arata_raspuns_card():
    s = st.session_state.get("studiu")
    if s:
        s["arata"] = True


def raspunde_card(stiu):
    """'Știu' scoate cardul din coadă; 'Nu știu' îl pune înapoi, la câteva
    carduri distanță, ca să revină curând."""
    s = st.session_state.get("studiu")
    if not s or not s["coada"]:
        return
    i = s["coada"].pop(0)
    s["incercari"] += 1
    if not stiu:
        s["gresite"][i] = s["gresite"].get(i, 0) + 1
        s["coada"].insert(min(3, len(s["coada"])), i)
    s["arata"] = False


def tab_carduri(ctx):
    st.caption(DESCRIERI_TAB["carduri"])
    nr_carduri = st.number_input("Număr flashcarduri", 5, 20, 10)

    if st.button("Generează flashcarduri"):
        with st.spinner("Pregătesc flashcardurile..."):
            try:
                carduri, model_folosit, nota = preia_din_teanc(
                    ("carduri", ctx.hash_material, ctx.limba),
                    nr_carduri,
                    "fata",
                    lambda: genereaza_teanc_carduri(
                        ctx.client, ctx.selectate, ctx.eticheta, ctx.limba
                    ),
                )
                st.session_state["carduri"] = carduri
                st.session_state["info_carduri"] = f"{model_folosit} · {nota}"
                porneste_studiu(len(carduri))
            except Exception as e_card:
                st.error(f"A apărut o eroare: {e_card}")

    carduri = st.session_state.get("carduri")
    if not carduri:
        return

    studiu = st.session_state.get("studiu")
    if not studiu or max(studiu["ids"], default=-1) >= len(carduri):
        porneste_studiu(len(carduri))
        studiu = st.session_state["studiu"]

    total_s = len(studiu["ids"])
    ramase = len(studiu["coada"])
    retinute = total_s - ramase

    st.caption(f"Model: {st.session_state.get('info_carduri', '?')}")
    st.download_button(
        "Descarcă flashcardurile pentru printat (.html)",
        data=html_carduri(carduri),
        file_name="flashcarduri.html",
        mime="text/html",
        on_click="ignore",
        key="dl_carduri",
    )
    st.progress(
        retinute / total_s if total_s else 1.0,
        text=f"Ai reținut {retinute} din {total_s} carduri",
    )

    if studiu["coada"]:
        i = studiu["coada"][0]
        card = carduri[i]
        greseli = studiu["gresite"].get(i, 0)

        with st.container(border=True):
            if greseli:
                st.caption("Revine pentru că ai greșit-o înainte")
            st.markdown("**Întrebare**")
            st.subheader(card.get("fata", ""))
            if studiu["arata"]:
                st.divider()
                st.markdown("**Răspuns**")
                st.write(card.get("spate", ""))
                st.caption(
                    f"{card.get('unitate', 'pagina').capitalize()} "
                    f"{card.get('pagina', '?')}"
                )

        if not studiu["arata"]:
            st.button(
                "Arată răspunsul",
                on_click=arata_raspuns_card,
                key="sr_arata",
                use_container_width=True,
            )
        else:
            b1, b2 = st.columns(2)
            b1.button(
                "Nu știu",
                on_click=raspunde_card,
                args=(False,),
                key="sr_nu",
                use_container_width=True,
            )
            b2.button(
                "Știu",
                on_click=raspunde_card,
                args=(True,),
                key="sr_stiu",
                use_container_width=True,
                type="primary",
            )
        st.caption(f"Mai ai {ramase} carduri de învățat în această rundă.")

    else:
        st.success("Ai terminat toate cardurile din această sesiune. Bravo!")
        gresite = studiu["gresite"]
        din_prima = sum(1 for k in studiu["ids"] if k not in gresite)

        m1, m2, m3 = st.columns(3)
        m1.metric("Știute din prima", f"{din_prima}/{total_s}")
        m2.metric("Încercări în total", studiu["incercari"])
        m3.metric("Carduri greșite măcar o dată", len(gresite))

        grele = sorted(gresite.items(), key=lambda x: -x[1])
        if grele:
            st.subheader("Cardurile la care ai greșit cel mai des")
            for k, nr_gres in grele[:5]:
                ori = "dată" if nr_gres == 1 else "ori"
                st.markdown(f"- **{carduri[k]['fata']}** (greșit de {nr_gres} {ori})")

        b1, b2 = st.columns(2)
        b1.button(
            "Studiază din nou toate",
            on_click=porneste_studiu,
            args=(len(carduri),),
            key="sr_toate",
            use_container_width=True,
        )
        if grele:
            b2.button(
                "Repetă doar cardurile dificile",
                on_click=porneste_studiu,
                args=(len(carduri), [k for k, _ in grele]),
                key="sr_grele",
                use_container_width=True,
            )


# ---------------- REZUMAT ----------------
def tab_rezumat(ctx):
    st.caption(DESCRIERI_TAB["rezumat"])
    nivel = st.selectbox("Cât de detaliat?", list(NIVELE_REZUMAT.keys()), index=1)

    if st.button("Generează rezumat"):
        cheie_rez = ("rezumat", ctx.hash_material, nivel, ctx.limba)
        salvat = citeste(cheie_rez)
        if salvat is not None:
            st.session_state["rezumat"] = salvat["text"]
            st.session_state["info_rezumat"] = (
                f"{salvat['model']} · din memorie, fără cerere nouă"
            )
        else:
            with st.spinner("Generez rezumatul..."):
                try:
                    rezumat, model_folosit = genereaza_rezumat(
                        ctx.client, ctx.selectate, ctx.eticheta, nivel, ctx.limba
                    )
                    salveaza(cheie_rez, {"text": rezumat, "model": model_folosit})
                    st.session_state["rezumat"] = rezumat
                    st.session_state["info_rezumat"] = (
                        f"{model_folosit} · cerere nouă la Google"
                    )
                except Exception as e_rez:
                    st.error(f"A apărut o eroare: {e_rez}")

    rezumat = st.session_state.get("rezumat")
    if rezumat:
        st.caption(f"Model: {st.session_state.get('info_rezumat', '?')}")
        st.markdown(rezumat)
        st.download_button(
            "Descarcă rezumatul (.txt)",
            data=rezumat,
            file_name="rezumat.txt",
            mime="text/plain",
            on_click="ignore",
            key="dl_rezumat",
        )


# ---------------- ÎNTREABĂ (caută în tot documentul) ----------------
def chat_curent(hash_doc):
    """Conversația e legată de documentul curent; la alt document începe de la zero."""
    chat = st.session_state.get("chat")
    if not chat or chat["hash"] != hash_doc:
        chat = {"hash": hash_doc, "mesaje": [], "folosite": 0}
        st.session_state["chat"] = chat
    return chat


def sterge_conversatia():
    chat = st.session_state.get("chat")
    if chat:
        chat["mesaje"] = []


def tab_intreaba(ctx):
    mat = ctx.mat
    chat = chat_curent(mat["hash"])

    st.caption(
        "Scrie o întrebare sau un concept pe care nu-l înțelegi și primești o "
        "explicație bazată doar pe document. Caut în tot documentul, nu doar "
        "în partea aleasă la pasul 1."
    )
    # loc rezervat: contorul se completează după procesarea întrebării
    contor = st.empty()
    zona_chat = st.container()

    with st.form("form_intreaba", clear_on_submit=True):
        intrebare = st.text_input(
            "Întrebarea ta",
            max_chars=MAX_LUNGIME_INTREBARE,
            placeholder="ex: Ce este ciclul Calvin? Explică mai simplu.",
        )
        trimis = st.form_submit_button("Întreabă")

    if trimis and intrebare.strip():
        intrebare = intrebare.strip()
        ramase_q = MAX_INTREBARI_SESIUNE - chat["folosite"]
        primul = len(chat["mesaje"]) == 0
        cheie_q = ("intreaba", mat["hash"], ctx.limba, norm(intrebare))
        salvat = citeste(cheie_q)

        if primul and salvat is not None:
            chat["mesaje"].append({"rol": "user", "text": intrebare})
            chat["mesaje"].append(
                {
                    "rol": "assistant",
                    "text": salvat["text"],
                    "info": f"{salvat['model']} · din memorie, fără cerere nouă",
                    "surse": salvat.get("surse", ""),
                }
            )
        elif ramase_q <= 0:
            st.warning(
                "Ai folosit toate întrebările din această sesiune. "
                "Revino mai târziu sau încearcă flashcardurile și rezumatul."
            )
        else:
            with st.spinner("Caut în document și mă gândesc..."):
                try:
                    ultima_q = next(
                        (m["text"] for m in reversed(chat["mesaje"]) if m["rol"] == "user"),
                        "",
                    )
                    fragmente, partial = alege_fragmente(mat, intrebare, ultima_q)
                    raspuns, model_folosit = raspunde_intrebare(
                        ctx.client,
                        fragmente,
                        ctx.eticheta,
                        partial,
                        intrebare,
                        chat["mesaje"],
                        ctx.limba,
                    )
                    surse = descrie_surse(fragmente, ctx.eticheta) if partial else ""
                    chat["folosite"] += 1
                    chat["mesaje"].append({"rol": "user", "text": intrebare})
                    chat["mesaje"].append(
                        {
                            "rol": "assistant",
                            "text": raspuns,
                            "info": f"{model_folosit} · cerere nouă la Google",
                            "surse": surse,
                        }
                    )
                    if primul:
                        salveaza(
                            cheie_q,
                            {"text": raspuns, "model": model_folosit, "surse": surse},
                        )
                except Exception as e_chat:
                    st.error(f"A apărut o eroare: {e_chat}")

    # afișăm contorul abia acum, după ce întrebarea a fost procesată
    ramase_acum = MAX_INTREBARI_SESIUNE - chat["folosite"]
    contor.caption(f"Întrebări rămase în această sesiune: {max(ramase_acum, 0)}")

    with zona_chat:
        for m in chat["mesaje"]:
            with st.chat_message(m["rol"]):
                st.markdown(m["text"])
                if m.get("info"):
                    st.caption(f"Model: {m['info']}")
                if m.get("surse"):
                    st.caption(m["surse"])

    if chat["mesaje"]:
        st.button("Șterge conversația", on_click=sterge_conversatia)
        st.caption(
            "Răspunsurile pot conține greșeli. Verifică sursa indicată în document."
        )
