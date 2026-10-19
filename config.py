"""Setări și texte fixe ale aplicației.

Aici se schimbă lucruri precum modelele folosite, limitele sau textele afișate.
"""

# Încearcă modelele în ordinea asta. Dacă unul e aglomerat sau epuizat,
# trece la următorul.
MODELE = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-flash-lite-latest",
]

# Cât text trimitem la o singură generare (aprox. 60 de pagini obișnuite)
MAX_CARACTERE = 150_000
MAX_CARACTERE_LIPIT = 300_000
TINTA_SECTIUNE = 3000  # mărimea unei "secțiuni" pentru fișiere fără pagini
NR_FRAGMENTE_INTREBARE = 10  # câte fragmente relevante caută "Întreabă"
MAX_DOCUMENTE_IN_MEMORIE = 200

# Câte elemente cerem dintr-o singură cerere (teancul)
DIM_TEANC_QUIZ = 30
DIM_TEANC_CARDURI = 40
DIM_TEANC_AF = 40

# Tipurile de întrebări din Quiz și Examen
TIP_GRILA = "Grilă (4 variante)"
TIP_AF = "Adevărat / Fals"
TIP_MIXT = "Mix (Grilă + Adevărat/Fals)"
TIPURI_INTREBARI = [TIP_GRILA, TIP_MIXT]

# Întrebări către Google permise pe sesiune în secțiunea "Întreabă"
MAX_INTREBARI_SESIUNE = 10
MAX_LUNGIME_INTREBARE = 500

NIVELE_REZUMAT = {
    "scurt": "foarte scurt, cam 150 de cuvinte",
    "mediu": "de lungime medie, cam 350 de cuvinte",
    "detaliat": "detaliat, cam 700 de cuvinte",
}

PLURAL = {"pagina": "pagini", "secțiunea": "secțiuni"}

# ------------------------- setări SAT -------------------------
SECTIUNI_SAT = {"Reading and Writing": "rw", "Math": "mate"}
NIVELE_SAT = {"ușoară": "easy", "medie": "medium", "grea": "hard"}
MINUTE_SAT = {"rw": 12, "mate": 16}  # pentru 10 întrebări
MAX_INTREBARI_SAT = 20
LIMBI_EN = {"română": "Romanian", "engleză": "English"}

TEME_SAT = {
    "rw": [
        "Words in Context",
        "Text Structure and Purpose",
        "Central Ideas and Details",
        "Command of Evidence (textual)",
        "Inferences",
        "Boundaries (punctuation between sentences and clauses)",
        "Form, Structure, and Sense (grammar)",
        "Transitions",
        "Rhetorical Synthesis (student notes)",
    ],
    "mate": [
        "Linear equations in one variable",
        "Linear equations in two variables",
        "Systems of two linear equations",
        "Linear inequalities",
        "Quadratic equations and functions",
        "Exponential growth and decay",
        "Polynomials and equivalent expressions",
        "Radicals and rational exponents",
        "Ratios, rates, and unit conversion",
        "Percentages",
        "Mean, median, and range",
        "Probability",
        "Interpreting linear models (slope and intercept in context)",
        "Area and volume",
        "Lines, angles, and triangles",
        "Right triangle trigonometry",
        "Circles (arc, sector, equation)",
    ],
}

DISCLAIMER_SAT = (
    "**Important:** întrebările sunt scrise de AI în stilul SAT-ului digital. "
    "**Nu sunt întrebări reale** din examenele trecute și pot conține greșeli, "
    "mai ales la matematică. Dacă o explicație nu te convinge, verific-o singur. "
    "Scorul de aici e doar procentul de răspunsuri corecte, nu scorul oficial "
    "400-1600. Pentru întrebări oficiale, folosește testele de practică gratuite "
    "de la College Board (aplicația Bluebook)."
)

# ------------------------- texte afișate în aplicație -------------------------
DESCRIERI_TAB = {
    "quiz": (
        "Întrebări grilă sau mix (grilă + Adevărat/Fals), din materialul tău, cu "
        "explicații și sursa fiecărui răspuns. Poți descărca quiz-ul pentru printat."
    ),
    "examen": (
        "Un test cu cronometru, cu întrebări grilă sau mix (grilă + Adevărat/Fals). "
        "La final primești scorul și un raport cu locurile din document la care "
        "ai greșit cel mai mult."
    ),
    "carduri": (
        "Flashcarduri cu repetare: apeși „Știu” sau „Nu știu”, iar cardurile "
        "greșite revin până le înveți."
    ),
    "rezumat": (
        "Rezumat scurt, mediu sau detaliat, cu sursele ideilor, pe care îl poți "
        "descărca."
    ),
    "intreaba": (
        "Pune o întrebare despre un concept pe care nu-l înțelegi și primești o "
        "explicație simplă, bazată doar pe documentul tău."
    ),
}

TEXT_GHID = """
**Cum folosești aplicația**

1. **Alege materialul.** Încarcă un PDF, un document Word sau un fișier text, ori
   lipește text cu Ctrl+V. La documentele lungi alegi partea pe care vrei s-o
   înveți (de exemplu un capitol).
2. **Alege ce vrei să faci** din secțiunile de mai jos.
3. **Învață și verifică.** Răspunsurile arată de unde vin în document (pagina sau
   secțiunea), ca să poți verifica.

**Secțiuni**

- **Quiz:** întrebări grilă sau mix cu Adevărat/Fals, cu explicații, care se pot printa.
- **Examen:** test cu cronometru și raport cu locurile la care ai greșit.
- **SAT:** întrebări în stilul SAT-ului digital, fără document. Merge direct,
  nu trebuie să încarci nimic.
- **Flashcarduri:** cu repetare, cardurile greșite revin până le știi.
- **Rezumat:** scurt, mediu sau detaliat.
- **Întreabă:** explicații simple, din documentul tău.

**Bine de știut**

- AI-ul poate greși. Verifică mereu sursa indicată.
- Aplicația folosește o limită gratuită, comună tuturor utilizatorilor. Dacă apare
  un mesaj că modelele sunt indisponibile sau limita e atinsă, încearcă mai târziu.
"""

TEXT_FOOTER = (
    "AI Study Buddy. Conținutul e generat de AI și poate conține greșeli. "
    "Textul din documentele tale este trimis la Google pentru generare, deci nu "
    "încărca materiale private. Pentru a economisi cereri, serverul păstrează "
    "temporar în memorie întrebările generate și textul extras din ultimele "
    "documente, până la repornirea aplicației."
)

CSS_APP = """
<style>
:root {
    --accent: #E5383B;
    --accent-soft: rgba(229, 56, 59, 0.12);
    --border: #2A2A30;
    --muted: #9B9BA1;
}

* {
    transition: background-color 0.15s ease, border-color 0.15s ease,
        color 0.15s ease, opacity 0.2s ease;
}

[data-testid="stMainBlockContainer"], .block-container {
    padding-top: 1.25rem;
    padding-bottom: 4rem;
    max-width: 760px;
}

h1 {
    font-weight: 800;
    letter-spacing: -0.02em;
}

h2, h3 {
    font-weight: 700;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Cardurile cu bordură (materiale salvate, secțiuni cu st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: 12px;
    border-color: var(--border) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover > div {
    border-color: var(--accent) !important;
}

/* Tab-uri */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}
[data-testid="stTabs"] button[role="tab"] {
    font-weight: 600;
    color: var(--muted);
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #D0D0D5;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--accent);
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: var(--accent);
    transition: left 0.25s ease, width 0.25s ease;
}

/* Butoane generale */
button {
    border-radius: 8px !important;
}
button:hover {
    transform: translateY(-1px);
}
button:active {
    transform: translateY(0);
}
button[kind="primary"] {
    background-color: var(--accent);
    border-color: var(--accent);
}
button[kind="primary"]:hover {
    background-color: #c92f32;
    border-color: #c92f32;
    box-shadow: 0 2px 10px rgba(229, 56, 59, 0.35);
}

/* Scoruri (st.metric) */
[data-testid="stMetric"] {
    background-color: var(--accent-soft);
    border-radius: 10px;
    padding: 0.75rem 1rem;
}
[data-testid="stMetric"]:hover {
    background-color: rgba(229, 56, 59, 0.18);
}

/* Bară de progres */
[data-testid="stProgress"] > div > div {
    background-color: var(--accent);
    transition: width 0.4s ease;
}

/* Alerte (success/info/warning/error) — intrare lină */
[data-testid="stAlert"] {
    border-radius: 10px;
    animation: strecura-sus 0.25s ease;
}

/* Conținut nou apărut (quiz generat, rezultate etc.) */
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] {
    animation: strecura-sus 0.2s ease;
}

@keyframes strecura-sus {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Butonul de profil: tras spre marginea stângă a ecranului, cu aspect de
   "pastilă" discretă, roșu doar la hover */
div[class*="st-key-profil_fixat"] {
    width: fit-content;
    margin-left: calc((760px - 100vw) / 2 + 1rem);
    margin-bottom: 1.5rem;
}
div[class*="st-key-profil_fixat"] button {
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
    background-color: rgba(255, 255, 255, 0.04) !important;
    padding: 0.4rem 1rem !important;
    font-weight: 600;
}
div[class*="st-key-profil_fixat"] button:hover {
    border-color: var(--accent) !important;
    background-color: var(--accent-soft) !important;
    color: var(--accent) !important;
}

@media (max-width: 640px) {
    h1 { font-size: 1.7rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    div[class*="st-key-profil_fixat"] {
        margin-left: 0;
    }
}
</style>
"""
