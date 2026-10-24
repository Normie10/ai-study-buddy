"""Textele traduse pentru Adevărat/Fals, Completează, Progresul meu și cardul
de obiectiv. Fiecare cheie are (text în română, text în engleză)."""

TEXTE_SECTIUNI = {
    # ---------- comune (Adevărat/Fals și Completează) ----------
    "sect.vezi_rezultat": ("Vezi rezultatul", "See the result"),
    "sect.urmatoarea": ("Următoarea", "Next"),
    "sect.corecte_pana_acum": (
        "Corecte până acum: {c} din {n}",
        "Correct so far: {c} of {n}",
    ),
    "sect.terminat": ("Ai terminat", "You finished"),
    "sect.scor": ("Scor", "Score"),
    "sect.procent": ("Procent", "Percent"),
    "sect.recapitulezi": ("Ce să recapitulezi", "What to review"),
    "sect.grup": ("**{eticheta}**: {n} {cuvant}", "**{eticheta}**: {n} {cuvant}"),
    "sect.raspuns_tau_corect": (
        "Răspunsul tău: {x}. Răspuns corect: {y}.",
        "Your answer: {x}. Correct answer: {y}.",
    ),
    "sect.fara_raspuns": ("fără răspuns", "no answer"),
    "sect.nou": ("Început nou", "Start over"),
    "sect.start": ("Începe", "Start"),
    # ---------- Adevărat / Fals ----------
    "af.nr": ("Număr afirmații", "Number of statements"),
    "af.spinner": ("Se generează afirmațiile...", "Generating the statements..."),
    "af.fara_elemente": (
        "Nu am găsit afirmații în acest material.",
        "I found no statements in this material.",
    ),
    "af.doar_n": (
        " (am găsit doar {n} afirmații distincte)",
        " (I found only {n} distinct statements)",
    ),
    "af.progres": ("Afirmația {i} din {total}", "Statement {i} of {total}"),
    "af.intrebare": ("Adevărat sau fals?", "True or false?"),
    "af.adevarat": ("Adevărat", "True"),
    "af.fals": ("Fals", "False"),
    "af.corect": ("Corect!", "Correct!"),
    "af.gresit": (
        "Greșit. Răspunsul corect: {r}.",
        "Wrong. The correct answer: {r}.",
    ),
    "af.toate_corecte": (
        "Ai răspuns corect la toate afirmațiile. Bravo!",
        "You answered all statements correctly. Well done!",
    ),
    "af.afirmatie_gresita": ("afirmație greșită", "wrong statement"),
    "af.afirmatii_gresite": ("afirmații greșite", "wrong statements"),
    "af.nota": (
        "Locurile indicate sunt cele date de model pentru fiecare afirmație. "
        "Verifică-le în document.",
        "The places shown are the ones given by the model for each statement. "
        "Check them in the document.",
    ),
    "af.vezi_gresite": ("Vezi afirmațiile greșite", "See the wrong statements"),
    "af.descarca": (
        "Descarcă afirmațiile pentru printat (.html)",
        "Download the statements to print (.html)",
    ),
    "af.repeta": (
        "Repetă doar afirmațiile greșite",
        "Repeat only the wrong statements",
    ),
    # ---------- Completează ----------
    "comp.spinner": ("Se generează întrebările...", "Generating the questions..."),
    "comp.fara_elemente": (
        "Nu am găsit întrebări potrivite în acest material.",
        "I found no suitable questions in this material.",
    ),
    "comp.doar_n": (
        " (am găsit doar {n} întrebări distincte)",
        " (I found only {n} distinct questions)",
    ),
    "comp.progres": ("Întrebarea {i} din {total}", "Question {i} of {total}"),
    "comp.eticheta": ("Completează spațiul liber:", "Fill in the blank:"),
    "comp.raspunsul_tau": ("Răspunsul tău", "Your answer"),
    "comp.verifica": ("Verifică", "Check"),
    "comp.corect": (
        "Corect! Ai scris: „{x}”.",
        "Correct! You wrote: “{x}”.",
    ),
    "comp.corect_aprox": (
        "Corect (ai greșit puțin scrierea). Ai scris: „{x}”, forma corectă e „{y}”.",
        "Correct (you misspelled it slightly). You wrote: “{x}”, the correct form "
        "is “{y}”.",
    ),
    "comp.gresit": (
        "Greșit. Ai scris: „{x}”. Răspunsul corect: {y}.",
        "Wrong. You wrote: “{x}”. The correct answer: {y}.",
    ),
    "comp.toate_corecte": (
        "Ai răspuns corect la toate întrebările. Bravo!",
        "You answered all questions correctly. Well done!",
    ),
    "comp.intrebare_gresita": ("întrebare greșită", "wrong question"),
    "comp.intrebari_gresite": ("întrebări greșite", "wrong questions"),
    "comp.nota": (
        "Locurile indicate sunt cele date de model pentru fiecare întrebare. "
        "Verifică-le în document.",
        "The places shown are the ones given by the model for each question. "
        "Check them in the document.",
    ),
    "comp.vezi_gresite": ("Vezi întrebările greșite", "See the wrong questions"),
    "comp.repeta": (
        "Repetă doar întrebările greșite",
        "Repeat only the wrong questions",
    ),
    # ---------- Progresul meu ----------
    "pr.tab.general": ("Prezentare generală", "Overview"),
    "pr.tab.istoric": ("Istoric", "History"),
    "pr.tip.quiz": ("Quiz", "Quiz"),
    "pr.tip.examen": ("Examen", "Exam"),
    "pr.tip.sat": ("SAT", "SAT"),
    "pr.tip.af": ("Adevărat/Fals", "True/False"),
    "pr.tip.comp": ("Completează", "Fill in the blank"),
    "pr.statistici": ("Statistici", "Statistics"),
    "pr.total": ("Total încercări", "Total attempts"),
    "pr.scor_mediu": ("Scor mediu", "Average score"),
    "pr.preferata": ("Secțiunea preferată", "Favorite section"),
    "pr.grafic_tip": ("Încercări pe tip", "Attempts by type"),
    "pr.grafic_timp": ("Evoluția scorului (%) în timp", "Score (%) over time"),
    "pr.vizitator": (
        "Progresul se salvează doar cu un cont. Creează unul gratuit din meniul "
        "de profil, ca să-ți vezi istoricul aici data viitoare.",
        "Progress is saved only with an account. Create a free one from the "
        "profile menu to see your history here next time.",
    ),
    "pr.eroare_incarcare": (
        "Nu am putut încărca progresul: {e}",
        "Could not load your progress: {e}",
    ),
    "pr.gol": (
        "Nu ai niciun rezultat salvat încă. Termină un quiz sau un examen.",
        "You have no saved results yet. Finish a quiz or an exam.",
    ),
    "pr.filtru": ("Arată doar", "Show only"),
    "pr.filtru_gol": (
        "Niciun rezultat pentru filtrul ales.",
        "No results for the selected filter.",
    ),
    "pr.favorite": ("Favorite", "Favorites"),
    "pr.tot": ("Tot istoricul", "Full history"),
    "pr.istoric": ("Istoric", "History"),
    "pr.eroare_update": ("Nu am putut actualiza: {e}", "Could not update: {e}"),
    "pr.favorit_ajutor": ("Marchează ca favorit", "Mark as favorite"),
    # ---------- cardul de obiectiv și serie ----------
    "ob.titlu": ("Obiectiv de azi", "Today's goal"),
    "ob.unit_activitati": ("activități terminate", "activities completed"),
    "ob.serie": ("Serie", "Streak"),
    "ob.la_rand": ("{unit} la rând", "{unit} in a row"),
    "ob.record": (
        "Cea mai lungă serie: {n} {unit}",
        "Longest streak: {n} {unit}",
    ),
    "ob.atins": ("Obiectiv atins azi. Bravo!", "Goal reached today. Well done!"),
    "ob.incepe": (
        "Termină un quiz sau un test ca să începi seria.",
        "Finish a quiz or a test to start your streak.",
    ),
    "ob.pastreaza": (
        "Termină o activitate azi ca să-ți păstrezi seria.",
        "Finish an activity today to keep your streak.",
    ),
    "ob.ramase": (
        "Mai ai {r} {cuvant} până la obiectiv.",
        "You have {r} {cuvant} left to reach the goal.",
    ),
    "ob.activitate": ("activitate", "activity"),
    "ob.activitati": ("activități", "activities"),
    "ob.serie_noua": ("Ai început o serie nouă!", "You started a new streak!"),
    "ob.zi_noua": (
        "Zi nouă în serie! Continuă și mâine.",
        "New day in your streak! Keep going tomorrow.",
    ),
    "ob.zile_sapt": ("LMMJVSD", "MTWTFSS"),
    "ob.eroare": (
        "Nu am putut încărca obiectivul zilnic acum.",
        "Could not load the daily goal right now.",
    ),
    "ob.schimba": ("Schimbă obiectivul", "Change the goal"),
    "ob.pe_zi": ("Activități pe zi", "Activities per day"),
    "ob.ce_numara": (
        "O activitate este un rezultat salvat: Quiz, Examen, SAT, Adevărat/Fals "
        "sau Completează. Flashcardurile nu se numără.",
        "An activity is a saved result: Quiz, Exam, SAT, True/False or Fill in "
        "the blank. Flashcards do not count.",
    ),
    "ob.salveaza": ("Salvează obiectivul", "Save the goal"),
    "ob.doar_sesiune": (
        "Nu am putut salva obiectivul pe cont; e valabil doar cât ții pagina deschisă.",
        "The goal could not be saved to your account; it is valid only while the "
        "page stays open.",
    ),
}
