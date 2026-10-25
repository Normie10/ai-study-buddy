"""Texte pentru documente.py (alegerea părții din document) și pentru notele
din memorie.py (perechi: română, engleză)."""

TEXTE_DOCUMENTE = {
    # ---------- documente.py ----------
    "doc.citesc": ("Citesc documentul...", "Reading the document..."),
    "doc.expander": (
        "Ce parte din document folosesc?",
        "Which part of the document should I use?",
    ),
    "doc.incape": (
        "Tot documentul încape într-o singură generare. "
        "Poți totuși să alegi doar o parte.",
        "The whole document fits in a single generation. "
        "You can still choose just a part.",
    ),
    "doc.prea_mult": (
        "Documentul are aproximativ {total} de caractere, prea mult pentru o "
        "singură generare. Alege o parte (maximum {max} de caractere odată). "
        "Secțiunea „Întreabă” caută oricum în tot documentul.",
        "The document has about {total} characters, too much for a single "
        "generation. Choose a part (at most {max} characters at a time). "
        "The “Ask” section searches the whole document anyway.",
    ),
    "doc.sari_cap": (
        "Sari la un capitol (din cuprinsul documentului)",
        "Jump to a chapter (from the table of contents)",
    ),
    "doc.alege_cap": (
        "Alege un capitol (opțional)",
        "Choose a chapter (optional)",
    ),
    "doc.interval": ("Interval ({unitate})", "Range ({unitate})"),
    "doc.fara_text_interval": (
        "În {unitate} {start}-{end} nu am găsit text. Alege alt interval.",
        "I found no text in {unitate} {start}-{end}. Choose another range.",
    ),
    "doc.prea_mare": (
        "Intervalul ales e prea mare pentru o singură generare, așa că folosesc "
        "doar {unitate} {start}-{ultimul}. Alege un interval mai mic ca să "
        "acoperi și restul.",
        "The chosen range is too large for a single generation, so I only use "
        "{unitate} {start}-{ultimul}. Choose a smaller range to cover the rest.",
    ),
    "doc.folosesc": (
        "Pentru quiz, examen, flashcarduri și rezumat folosesc {unitate} "
        "{start}-{end} (aprox. {car} de caractere).",
        "For the quiz, exam, flashcards and summary I use {unitate} "
        "{start}-{end} (about {car} characters).",
    ),
    "doc.cautat": (
        "Am căutat în {unitate}: {lista}",
        "I searched in {unitate}: {lista}",
    ),
    # ---------- note din memorie.py ----------
    "mem.din_memorie": (
        "din memorie, fără cerere nouă la Google",
        "from memory, no new request to Google",
    ),
    "mem.cerere_noua": ("cerere nouă la Google", "new request to Google"),
    "mem.aglomerat_quiz": (
        "Google e aglomerat sau limita e atinsă, așa că am refolosit elemente "
        "din memorie",
        "Google is busy or the limit was reached, so I reused items from memory",
    ),
    "mem.aglomerat_examen": (
        "Google e aglomerat sau limita e atinsă, așa că am folosit întrebările "
        "din memorie",
        "Google is busy or the limit was reached, so I used the questions from "
        "memory",
    ),
    "mem.repetari": ("(unele se pot repeta)", "(some may repeat)"),
}
