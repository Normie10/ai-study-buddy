"""Traducerea interfeței (română / engleză).

Toate textele traduse stau aici, într-un singur loc: fiecare cheie are o pereche
(text în română, text în engleză). În cod se scrie t("cheie").
"""

import streamlit as st

from baza_date import _client, utilizator_curent

# Limbile oferite utilizatorilor. Cât timp traducerea nu e gata în toate
# fișierele, lasă doar ("ro",): selectorul de limbă nu apare, iar aplicația
# rămâne în română. Pentru a testa engleza, pune ("ro", "en").
LIMBI_DISPONIBILE = ("ro", "en")
NUME_LIMBA = {"ro": "Română", "en": "English"}


# ------------------------- limba aleasă -------------------------
def limba_ui():
    """Limba interfeței: „ro” sau „en”."""
    if len(LIMBI_DISPONIBILE) < 2:
        return "ro"
    din_sesiune = st.session_state.get("limba_ui")
    if din_sesiune in LIMBI_DISPONIBILE:
        return din_sesiune
    user = utilizator_curent()
    if user is not None:
        meta = getattr(user, "user_metadata", None) or {}
        cod = meta.get("limba_ui")
        if cod in LIMBI_DISPONIBILE:
            return cod
    return "ro"


def seteaza_limba_ui(cod):
    if cod not in LIMBI_DISPONIBILE:
        return
    st.session_state["limba_ui"] = cod
    if utilizator_curent() is None:
        return
    try:
        rezultat = _client().auth.update_user({"data": {"limba_ui": cod}})
        if rezultat is not None and rezultat.user is not None:
            st.session_state["utilizator"] = rezultat.user
    except Exception:
        pass  # rămâne valabilă pentru sesiunea curentă


def _la_schimbare_limba():
    seteaza_limba_ui(st.session_state["limba_ui_sel"])


def selector_limba():
    """Alegerea limbii, în meniul de profil. Apare doar dacă sunt cel puțin
    două limbi disponibile."""
    if len(LIMBI_DISPONIBILE) < 2:
        return
    coduri = list(LIMBI_DISPONIBILE)
    st.radio(
        t("profil.limba"),
        coduri,
        index=coduri.index(limba_ui()),
        format_func=lambda c: NUME_LIMBA[c],
        horizontal=True,
        key="limba_ui_sel",
        on_change=_la_schimbare_limba,
    )


# ------------------------- traducerea -------------------------
def t(cheie, **valori):
    """Textul pentru cheia dată, în limba aleasă. Valorile din {acolade} se
    completează cu cele date, de exemplu t("profil.sterge.eroare", e=eroare)."""
    pereche = TEXTE.get(cheie)
    if pereche is None:
        return cheie
    text = pereche[1] if limba_ui() == "en" else pereche[0]
    return text.format(**valori) if valori else text


def nume_tab(nume):
    """Numele tradus al unei secțiuni (sau cel original, dacă nu are traducere)."""
    return t(f"tab.{nume}") if f"tab.{nume}" in TEXTE else nume


def descriere_sectiune(nume, implicit=""):
    cheie = f"desc.{nume}"
    return t(cheie) if cheie in TEXTE else implicit


def unitate_ui(eticheta):
    """„pagini” / „secțiuni” (sau pages / sections)."""
    cheie = f"unitate.{eticheta}"
    return t(cheie) if cheie in TEXTE else eticheta


TEXTE = {
    # ---------- antet ----------
    "hero.titlu": ("AI Study Buddy", "AI Study Buddy"),
    "hero.sub": (
        "Transformă materialele tale în quiz-uri, teste cu cronometru, "
        "flashcarduri și rezumate.",
        "Turn your materials into quizzes, timed tests, flashcards and summaries.",
    ),
    # ---------- navigare ----------
    "nav.grupa.exerseaza": ("Exersează", "Practice"),
    "nav.grupa.invata": ("Învață", "Learn"),
    "nav.grupa.progres": ("Progres", "Progress"),
    "nav.grupa.altele": ("Altele", "More"),
    "tab.Quiz": ("Quiz", "Quiz"),
    "tab.Examen": ("Examen", "Exam"),
    "tab.SAT": ("SAT", "SAT"),
    "tab.Flashcarduri": ("Flashcarduri", "Flashcards"),
    "tab.Rezumat": ("Rezumat", "Summary"),
    "tab.Întreabă": ("Întreabă", "Ask"),
    "tab.Adevărat / Fals": ("Adevărat / Fals", "True / False"),
    "tab.Completează": ("Completează", "Fill in the blank"),
    "tab.Progresul meu": ("Progresul meu", "My progress"),
    # ---------- descrierile secțiunilor ----------
    "desc.Quiz": (
        "Întrebări grilă sau mix (grilă + Adevărat/Fals), din materialul tău, cu "
        "explicații și sursa fiecărui răspuns. Poți descărca quiz-ul pentru printat.",
        "Multiple-choice or mixed questions (multiple choice + True/False) from your "
        "material, with explanations and the source of each answer. You can download "
        "the quiz to print.",
    ),
    "desc.Examen": (
        "Un test cu cronometru, cu întrebări grilă sau mix (grilă + Adevărat/Fals). "
        "La final primești scorul și un raport cu locurile din document la care "
        "ai greșit cel mai mult.",
        "A timed test with multiple-choice or mixed questions. At the end you get "
        "your score and a report on the places in the document where you made the "
        "most mistakes.",
    ),
    "desc.SAT": (
        "Întrebări în stilul SAT-ului digital, fără document.",
        "Digital SAT-style questions, no document needed.",
    ),
    "desc.Flashcarduri": (
        "Flashcarduri cu repetare: apeși „Știu” sau „Nu știu”, iar cardurile "
        "greșite revin până le înveți.",
        "Flashcards with repetition: press “I know” or “I don’t know”, and the cards "
        "you miss come back until you learn them.",
    ),
    "desc.Rezumat": (
        "Rezumat scurt, mediu sau detaliat, cu sursele ideilor, pe care îl poți "
        "descărca.",
        "A short, medium or detailed summary with the sources of the ideas, which "
        "you can download.",
    ),
    "desc.Întreabă": (
        "Pune o întrebare despre un concept pe care nu-l înțelegi și primești o "
        "explicație simplă, bazată doar pe documentul tău.",
        "Ask about a concept you don’t understand and get a simple explanation "
        "based only on your document.",
    ),
    "desc.Adevărat / Fals": (
        "Afirmații din materialul tău. Răspunzi pe rând cu Adevărat sau Fals și vezi "
        "imediat dacă ai nimerit, cu explicație și sursa din document.",
        "Statements from your material. Answer True or False one at a time and see "
        "right away if you got it right, with an explanation and the source in the "
        "document.",
    ),
    "desc.Completează": (
        "Propoziții din materialul tău, cu un cuvânt lipsă. Scrii răspunsul și vezi "
        "imediat dacă ai nimerit, cu explicație și sursa din document.",
        "Sentences from your material with a missing word. Type the answer and see "
        "right away if you got it right, with an explanation and the source in the "
        "document.",
    ),
    "desc.Progresul meu": (
        "Istoricul scorurilor tale la Quiz, Examen, SAT, Adevărat/Fals și "
        "Completează, cu statistici și grafice. Poți marca rezultatele importante "
        "cu o steluță și poți filtra după tip.",
        "Your score history for Quiz, Exam, SAT, True/False and Fill in the blank, "
        "with statistics and charts. You can star important results and filter by "
        "type.",
    ),
    # ---------- pașii paginii ----------
    "pas.1": ("Alege materialul", "Choose your material"),
    "pas.2": ("Alege ce vrei să faci", "Choose what to do"),
    "gol.titlu": ("Alege mai întâi un material", "Choose a material first"),
    "gol.indiciu": (
        "Pasul 1, mai sus: încarcă un fișier sau lipește text",
        "Step 1, above: upload a file or paste text",
    ),
    # ---------- pasul 1: materialul ----------
    "material.limba": (
        "Limba întrebărilor și a explicațiilor",
        "Language of questions and explanations",
    ),
    "material.limba.help": (
        "La SAT, întrebările rămân în engleză; explicațiile urmează această limbă.",
        "In SAT, the questions stay in English; the explanations follow this language.",
    ),
    "limba.romana": ("Română", "Romanian"),
    "limba.engleza": ("Engleză", "English"),
    "material.sursa": ("Sursa materialului", "Material source"),
    "material.sursa.help": (
        "Pentru SAT nu ai nevoie de material.",
        "You don’t need a material for SAT.",
    ),
    "sursa.fisier": ("Încarcă un fișier", "Upload a file"),
    "sursa.text": ("Lipește text", "Paste text"),
    "material.fisier": (
        "PDF, Word (.docx) sau text (.txt, .md)",
        "PDF, Word (.docx) or text (.txt, .md)",
    ),
    "material.fisier.eroare": (
        "Nu am putut citi fișierul: {e}",
        "Could not read the file: {e}",
    ),
    "material.text.eticheta": (
        "Lipește aici textul (Ctrl+V). Maximum {max} de caractere.",
        "Paste the text here (Ctrl+V). Maximum {max} characters.",
    ),
    "material.text.buton": ("Folosește acest text", "Use this text"),
    "material.text.sterge": ("Șterge textul", "Clear text"),
    "material.text.salveaza": (
        "Salvează acest material pe cont",
        "Save this material to my account",
    ),
    "material.text.salvat": ("Material salvat pe cont.", "Material saved to your account."),
    "material.text.eroare_salvare": ("Nu am putut salva: {e}", "Could not save: {e}"),
    "material.fara_text": (
        "Nu am găsit text în document. Dacă e un PDF scanat (poze cu text), "
        "momentan nu pot citi text din imagini.",
        "I found no text in the document. If it is a scanned PDF (pictures of "
        "text), I can’t read text from images yet.",
    ),
    "material.gata": (
        "{nume}: {n} {unitate}, aproximativ {car} de caractere",
        "{nume}: {n} {unitate}, about {car} characters",
    ),
    "material.text_lipit": ("Text lipit", "Pasted text"),
    "unitate.pagina": ("pagini", "pages"),
    "unitate.secțiunea": ("secțiuni", "sections"),
    # ---------- meniul de profil ----------
    "profil.incercari": ("Încercări", "Attempts"),
    "profil.scor_mediu": ("Scor mediu", "Average score"),
    "profil.fara_rezultate": ("Niciun rezultat salvat încă.", "No saved results yet."),
    "profil.materiale": ("Materialele mele", "My materials"),
    "profil.materiale.eroare": (
        "Nu am putut încărca materialele: {e}",
        "Could not load your materials: {e}",
    ),
    "profil.materiale.gol": ("Niciun material salvat încă.", "No saved materials yet."),
    "profil.incarca": ("Încarcă", "Load"),
    "profil.sterge": ("Șterge", "Delete"),
    "profil.sterge.eroare": ("Nu am putut șterge: {e}", "Could not delete: {e}"),
    "profil.delogare": ("Delogare", "Log out"),
    "profil.vizitator": (
        "Ești vizitator — materialele și progresul nu se salvează.",
        "You are a guest — materials and progress are not saved.",
    ),
    "profil.vizitator.eticheta": ("Vizitator", "Guest"),
    "profil.limba": ("Limba interfeței", "Interface language"),
    # ---------- ghid, avertismente, subsol ----------
    "ghid.titlu": ("Cum funcționează?", "How does it work?"),
    "ghid.adaugate": ("Secțiuni adăugate", "Added sections"),
    "ghid.text": (
        """
**Cum folosești aplicația**

1. **Alege materialul.** Încarcă un PDF, un document Word sau un fișier text, ori
   lipește text cu Ctrl+V. La documentele lungi alegi partea pe care vrei s-o
   înveți (de exemplu un capitol).
2. **Alege ce vrei să faci** din cele trei grupuri de mai jos.
3. **Învață și verifică.** Răspunsurile arată de unde vin în document (pagina sau
   secțiunea), ca să poți verifica.

**Grupuri și secțiuni**

- **Exersează:** Quiz, Examen cu cronometru, Adevărat / Fals, Completează și SAT
  (fără document, merge direct).
- **Învață:** Flashcarduri cu repetare, Rezumat și Întreabă (explicații simple,
  din documentul tău).
- **Progres:** istoricul scorurilor, obiectivul zilnic și seria de zile.

**Bine de știut**

- AI-ul poate greși. Verifică mereu sursa indicată.
- Aplicația folosește o limită gratuită, comună tuturor utilizatorilor. Dacă apare
  un mesaj că modelele sunt indisponibile sau limita e atinsă, încearcă mai târziu.
""",
        """
**How to use the app**

1. **Choose your material.** Upload a PDF, a Word document or a text file, or
   paste text with Ctrl+V. For long documents you pick the part you want to
   study (for example a chapter).
2. **Choose what to do** from the three groups below.
3. **Learn and check.** The answers show where they come from in the document
   (page or section), so you can verify them.

**Groups and sections**

- **Practice:** Quiz, timed Exam, True / False, Fill in the blank and SAT
  (no document needed).
- **Learn:** Flashcards with repetition, Summary and Ask (simple explanations
  from your own document).
- **Progress:** your score history, daily goal and streak.

**Good to know**

- AI can make mistakes. Always check the source shown.
- The app uses a free quota shared by all users. If a message says the models
  are unavailable or the limit was reached, try again later.
""",
    ),
    "avert.salvare": (
        "Scorul nu s-a putut salva pe cont, deci nu va apărea la „Progresul meu”. "
        "Rezultatul afișat este corect. Dacă mesajul se repetă, delogheaz-te și "
        "intră din nou în cont.",
        "Your score could not be saved to your account, so it will not appear in "
        "“My progress”. The result shown is correct. If this message keeps "
        "appearing, log out and sign in again.",
    ),
    "avert.detalii": ("Detalii tehnice: {motiv}", "Technical details: {motiv}"),
    "avert.inchide": ("Am înțeles", "Got it"),
    "footer": (
        "AI Study Buddy. Conținutul e generat de AI și poate conține greșeli. "
        "Textul din documentele tale este trimis la Google pentru generare, deci nu "
        "încărca materiale private. Pentru a economisi cereri, serverul păstrează "
        "temporar în memorie întrebările generate și textul extras din ultimele "
        "documente, până la repornirea aplicației.",
        "AI Study Buddy. The content is generated by AI and may contain mistakes. "
        "The text from your documents is sent to Google for generation, so do not "
        "upload private materials. To save requests, the server temporarily keeps "
        "the generated questions and the text extracted from the latest documents "
        "in memory until the app restarts.",
    ),
    # ---------- erori ----------
    "eroare.cheie_api": (
        "Lipsește cheia API. Verifică fișierul .env sau setările Secrets.",
        "The API key is missing. Check the .env file or the Secrets settings.",
    ),
    "eroare.sectiune_noua": (
        "O secțiune nouă nu s-a putut încărca ({eroare}). Restul aplicației merge normal.",
        "A new section could not be loaded ({eroare}). The rest of the app works normally.",
    ),
    "eroare.sectiune": (
        "Secțiunea „{nume}” a dat o eroare: {e}",
        "The section “{nume}” raised an error: {e}",
    ),
}

# ------------------------- texte pentru taburile de bază -------------------------
from texte_taburi import TEXTE_TABURI  # noqa: E402

TEXTE.update(TEXTE_TABURI)


def unitate_sg(unitate, majuscula=False):
    """„pagina” / „secțiunea” (sau page / section), la singular."""
    cheie = f"unitate1.{unitate}"
    text = t(cheie) if cheie in TEXTE else str(unitate)
    return text.capitalize() if majuscula else text


def sursa_ui(q):
    """De unde provine o întrebare: tema (SAT) sau pagina/secțiunea."""
    if q.get("tema"):
        return q["tema"]
    return f"{unitate_sg(q.get('unitate', 'pagina'))} {q.get('pagina', '?')}"


def eticheta_grup_ui(q):
    """Eticheta după care se grupează greșelile în raportul de la examen."""
    if q.get("tema"):
        return q["tema"]
    u = unitate_sg(q.get("unitate", "pagina"), majuscula=True)
    p = str(q.get("pagina", "?"))
    return t("grup.necunoscuta", u=u) if p == "?" else f"{u} {p}"


def text_intrebare_ui(q):
    """Textul întrebării, cu „Adevărat sau fals” la afirmații."""
    if q.get("tip_intrebare") == "af":
        return t("af.prefix", intrebare=q["intrebare"])
    return q["intrebare"]

# ------------------------- texte pentru secțiunile din sectiuni/ -------------------------
from texte_sectiuni import TEXTE_SECTIUNI  # noqa: E402

TEXTE.update(TEXTE_SECTIUNI)

from texte_autentificare import TEXTE_AUTENTIFICARE
TEXTE.update(TEXTE_AUTENTIFICARE)

from texte_abonamente import TEXTE_ABONAMENTE
TEXTE.update(TEXTE_ABONAMENTE)
