"""Textele traduse pentru Quiz, Examen, SAT, Flashcarduri, Rezumat și Întreabă.
Fiecare cheie are (text în română, text în engleză). Se încarcă din limbi.py."""

TEXTE_TABURI = {
    # ---------- comune ----------
    "comun.model": ("Model: {info}", "Model: {info}"),
    "comun.eroare": ("A apărut o eroare: {e}", "An error occurred: {e}"),
    "comun.dificultate": ("Dificultate", "Difficulty"),
    "comun.nr_intrebari": ("Număr întrebări", "Number of questions"),
    "comun.tip_intrebari": ("Tip de întrebări", "Question type"),
    "comun.timp": ("Timp (minute)", "Time (minutes)"),
    "comun.recapitulare": ("Recapitulare greșeli", "Mistakes review"),
    "comun.din_memorie": ("din memorie, fără cerere nouă", "from memory, no new request"),
    "comun.cerere_noua": ("cerere nouă la Google", "new request to Google"),
    "comun.fara_material": (
        "Încarcă un document (sau lipește text) la pasul 1 ca să începi.",
        "Upload a document (or paste text) in step 1 to get started.",
    ),
    "dif.ușoară": ("Ușoară", "Easy"),
    "dif.medie": ("Medie", "Medium"),
    "dif.grea": ("Grea", "Hard"),
    "tip.grila": ("Grilă (4 variante)", "Multiple choice (4 options)"),
    "tip.mixt": (
        "Mix (Grilă + Adevărat/Fals)",
        "Mixed (multiple choice + True/False)",
    ),
    "tip.af": ("Adevărat / Fals", "True / False"),
    "af.prefix": ("Adevărat sau fals: {intrebare}", "True or false: {intrebare}"),
    "unitate1.pagina": ("pagina", "page"),
    "unitate1.secțiunea": ("secțiunea", "section"),
    "grup.necunoscuta": ("{u} necunoscută", "{u} unknown"),
    # ---------- explicații ----------
    "expl.de_ce": ("De ce varianta ta e greșită:", "Why your answer is wrong:"),
    "expl.corect": ("Răspuns corect: {r}", "Correct answer: {r}"),
    "expl.gresit_quiz": (
        "{i}. Greșit. Răspuns corect: {corect}",
        "{i}. Wrong. Correct answer: {corect}",
    ),
    # ---------- quiz ----------
    "quiz.genereaza": ("Generează quiz", "Generate quiz"),
    "quiz.spinner": ("Se generează quiz-ul...", "Generating the quiz..."),
    "quiz.titlu": ("Quiz", "Quiz"),
    "quiz.descarca": (
        "Descarcă quiz-ul pentru printat (.html)",
        "Download the quiz to print (.html)",
    ),
    "quiz.preda": ("Predă răspunsurile", "Submit answers"),
    "quiz.corect": ("{i}. Corect!", "{i}. Correct!"),
    "quiz.scor": ("Scor: {scor}/{total}", "Score: {scor}/{total}"),
    "quiz.recap": (
        "Recapitulează doar greșelile ({n})",
        "Review only the mistakes ({n})",
    ),
    "quiz.predat_nota": (
        "Răspunsurile au fost predate. Pentru o nouă încercare, generează un quiz nou.",
        "Your answers have been submitted. For a new attempt, generate a new quiz.",
    ),
    # ---------- examen ----------
    "ex.start": ("Începe examenul", "Start the exam"),
    "ex.spinner": ("Se generează examenul...", "Generating the exam..."),
    "ex.preda": ("Predă examenul", "Submit the exam"),
    "ex.mai_putine": (
        "Am găsit doar {n} întrebări distincte, așa că testul are mai puține decât ai cerut.",
        "I found only {n} distinct questions, so the test has fewer than you asked for.",
    ),
    "ex.timp_ramas": ("Timp rămas", "Time left"),
    "ex.sub_minut": ("Mai ai sub un minut!", "Less than a minute left!"),
    "ex.expirat": (
        "Timpul a expirat. Întrebările fără răspuns au fost socotite greșite.",
        "Time is up. Unanswered questions were counted as wrong.",
    ),
    "ex.scor": ("Scor", "Score"),
    "ex.procent": ("Procent", "Percent"),
    "ex.timp_folosit": ("Timp folosit", "Time used"),
    "ex.fara_raspuns": (
        "Ai lăsat {n} întrebări fără răspuns.",
        "You left {n} questions unanswered.",
    ),
    "ex.recapitulezi": ("Ce să recapitulezi", "What to review"),
    "ex.toate_corecte": (
        "Ai răspuns corect la toate întrebările. Bravo!",
        "You answered all questions correctly. Well done!",
    ),
    "ex.intrebare_gresita": ("întrebare greșită", "wrong question"),
    "ex.intrebari_gresite": ("întrebări greșite", "wrong questions"),
    "ex.grup": (
        "**{eticheta}**: {g} din {tot} {cuvant}",
        "**{eticheta}**: {g} of {tot} {cuvant}",
    ),
    "ex.nota_sat": (
        "Temele sunt cele atribuite de model fiecărei întrebări.",
        "The topics are the ones assigned by the model to each question.",
    ),
    "ex.nota_doc": (
        "Locurile indicate sunt cele date de model pentru fiecare întrebare. "
        "Verifică-le în document.",
        "The places shown are the ones given by the model for each question. "
        "Check them in the document.",
    ),
    "ex.nota_sat_oficial": (
        "Întrebările sunt scrise de AI și pot conține greșeli. Scorul nu este "
        "scorul oficial SAT.",
        "The questions are written by AI and may contain mistakes. The score is "
        "not the official SAT score.",
    ),
    "ex.recap_buton": (
        "Recapitulează doar greșelile ({n})",
        "Review only the mistakes ({n})",
    ),
    "ex.vezi_toate": (
        "Vezi toate întrebările și răspunsurile",
        "See all questions and answers",
    ),
    "ex.corect": ("Corect", "Correct"),
    "ex.gresit": ("Greșit", "Wrong"),
    "ex.raspunsul_tau": ("Răspunsul tău: {r}", "Your answer: {r}"),
    "ex.fara_raspuns_text": ("fără răspuns", "no answer"),
    "ex.descarca": (
        "Descarcă rezultatele pentru printat (.html)",
        "Download the results to print (.html)",
    ),
    "ex.nou": ("Examen nou", "New exam"),
    # ---------- SAT ----------
    "sat.intro": (
        "Întrebări în stilul SAT-ului digital, **fără legătură cu documentul** "
        "încărcat. Întrebările sunt în engleză; explicațiile urmează limba "
        "aleasă mai sus.",
        "Digital SAT-style questions, **unrelated to the document** you uploaded. "
        "The questions are in English; the explanations follow the language "
        "chosen above.",
    ),
    "sat.disclaimer": (
        "**Important:** întrebările sunt scrise de AI în stilul SAT-ului digital. "
        "**Nu sunt întrebări reale** din examenele trecute și pot conține greșeli, "
        "mai ales la matematică. Dacă o explicație nu te convinge, verific-o singur. "
        "Scorul de aici e doar procentul de răspunsuri corecte, nu scorul oficial "
        "400-1600. Pentru întrebări oficiale, folosește testele de practică gratuite "
        "de la College Board (aplicația Bluebook).",
        "**Important:** the questions are written by AI in the style of the digital "
        "SAT. **They are not real questions** from past exams and may contain "
        "mistakes, especially in math. If an explanation does not convince you, "
        "check it yourself. The score here is only the percentage of correct "
        "answers, not the official 400-1600 score. For official questions, use the "
        "free practice tests from College Board (the Bluebook app).",
    ),
    "sat.sectiune": ("Secțiune", "Section"),
    "sat.timp_nota": (
        "Timpul implicit e calculat după ritmul de pe SAT-ul digital "
        "(în jur de 71 de secunde pe întrebare la Reading and Writing și 95 la "
        "Math). Verifică formatul actual pe collegeboard.org.",
        "The default time is based on the pace of the digital SAT (about 71 seconds "
        "per question in Reading and Writing and 95 in Math). Check the current "
        "format on collegeboard.org.",
    ),
    "sat.start": ("Începe testul SAT", "Start the SAT test"),
    "sat.spinner": ("Se generează testul SAT...", "Generating the SAT test..."),
    # ---------- flashcarduri ----------
    "fc.nr": ("Număr flashcarduri", "Number of flashcards"),
    "fc.genereaza": ("Generează flashcarduri", "Generate flashcards"),
    "fc.spinner": ("Se generează flashcardurile...", "Generating the flashcards..."),
    "fc.descarca": (
        "Descarcă flashcardurile pentru printat (.html)",
        "Download the flashcards to print (.html)",
    ),
    "fc.progres": (
        "Ai reținut {r} din {t} carduri",
        "You remembered {r} of {t} cards",
    ),
    "fc.revine": (
        "Revine pentru că ai greșit-o înainte",
        "Back because you missed it before",
    ),
    "fc.intrebare": ("Întrebare", "Question"),
    "fc.raspuns": ("Răspuns", "Answer"),
    "fc.arata": ("Arată răspunsul", "Show answer"),
    "fc.nu_stiu": ("Nu știu", "I don't know"),
    "fc.stiu": ("Știu", "I know"),
    "fc.mai_ai": (
        "Mai ai {n} carduri de învățat în această rundă.",
        "You have {n} cards left to learn in this round.",
    ),
    "fc.terminat": (
        "Ai terminat toate cardurile din această sesiune. Bravo!",
        "You finished all the cards in this session. Well done!",
    ),
    "fc.din_prima": ("Știute din prima", "Known on the first try"),
    "fc.incercari": ("Încercări în total", "Total attempts"),
    "fc.gresite_macar": ("Carduri greșite măcar o dată", "Cards missed at least once"),
    "fc.cele_mai_grele": (
        "Cardurile la care ai greșit cel mai des",
        "The cards you missed most often",
    ),
    "fc.greseli": ("{card} (greșit de {n} {ori})", "{card} (missed {n} {ori})"),
    "fc.ori1": ("dată", "time"),
    "fc.orin": ("ori", "times"),
    "fc.toate": ("Studiază din nou toate", "Study all again"),
    "fc.dificile": ("Repetă doar cardurile dificile", "Repeat only the hard cards"),
    # ---------- rezumat ----------
    "rz.detaliat": ("Cât de detaliat?", "How detailed?"),
    "rz.nivel.scurt": ("Scurt", "Short"),
    "rz.nivel.mediu": ("Mediu", "Medium"),
    "rz.nivel.detaliat": ("Detaliat", "Detailed"),
    "rz.genereaza": ("Generează rezumat", "Generate summary"),
    "rz.spinner": ("Se generează rezumatul...", "Generating the summary..."),
    "rz.descarca": ("Descarcă rezumatul (.txt)", "Download the summary (.txt)"),
    # ---------- întreabă ----------
    "int.intro": (
        "Scrie o întrebare sau un concept pe care nu-l înțelegi și primești o "
        "explicație bazată doar pe document. Caut în tot documentul, nu doar "
        "în partea aleasă la pasul 1.",
        "Write a question or a concept you don't understand and get an explanation "
        "based only on the document. I search the whole document, not only the "
        "part chosen in step 1.",
    ),
    "int.eticheta": ("Întrebarea ta", "Your question"),
    "int.placeholder": (
        "ex: Ce este ciclul Calvin? Explică mai simplu.",
        "e.g. What is the Calvin cycle? Explain it more simply.",
    ),
    "int.buton": ("Întreabă", "Ask"),
    "int.limita": (
        "Ai folosit toate întrebările din această sesiune. "
        "Revino mai târziu sau încearcă flashcardurile și rezumatul.",
        "You have used all the questions in this session. Come back later or "
        "try the flashcards and the summary.",
    ),
    "int.spinner": (
        "Se caută răspunsul în document...",
        "Searching the document for the answer...",
    ),
    "int.ramase": (
        "Întrebări rămase în această sesiune: {n}",
        "Questions left in this session: {n}",
    ),
    "int.sterge": ("Șterge conversația", "Clear the conversation"),
    "int.avert": (
        "Răspunsurile pot conține greșeli. Verifică sursa indicată în document.",
        "Answers may contain mistakes. Check the source shown in the document.",
    ),
}
