"""Setări fixe ale aplicației.

Aici se schimbă lucruri precum modelele folosite, limitele sau stilul aplicației.
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

# ------------------------- stilul aplicației (CSS) -------------------------
CSS_APP = """
<style>
:root {
    --accent: #E5383B;
    --accent-soft: rgba(229, 56, 59, 0.10);
    --accent-glow: rgba(229, 56, 59, 0.30);
    --border: #2A2A30;
    --border-hover: #3C3C45;
    --surface: rgba(255, 255, 255, 0.03);
    --muted: #9B9BA1;
    --latime: 920px;
    --raza: 12px;
}

::selection {
    background: rgba(229, 56, 59, 0.35);
}

/* Bara de sus a Streamlit: transparentă, ca să nu taie conținutul */
[data-testid="stHeader"] {
    background: transparent;
}

/* Blocul care conține doar acest stil nu trebuie să ocupe loc în pagină */
[data-testid="stElementContainer"]:has(style) {
    display: none;
}

[data-testid="stMainBlockContainer"], .block-container {
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    max-width: var(--latime);
}

/* ---------- Text ---------- */
h1 {
    font-weight: 800;
    letter-spacing: -0.025em;
}
h2, h3 {
    font-weight: 700;
    letter-spacing: -0.015em;
}
/* Textele mici (descrieri, explicații): lizibile, nu stinse. Culoarea se pune
   și pe elementele dinăuntru, fiindcă Streamlit le dă o transparență proprie. */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: var(--muted) !important;
    opacity: 1 !important;
}
hr {
    border-color: var(--border) !important;
}

/* ---------- Antet ---------- */
.hero {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.25rem 0 1.25rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    animation: aparitie 0.5s ease both;
}
.hero-marca {
    flex-shrink: 0;
    width: 10px;
    height: 46px;
    border-radius: 6px;
    background: linear-gradient(180deg, #F0494C 0%, #B8282B 100%);
    box-shadow: 0 0 20px rgba(229, 56, 59, 0.45);
}
.hero-titlu {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.hero-sub {
    margin-top: 0.4rem;
    color: var(--muted);
    font-size: 0.95rem;
    line-height: 1.4;
}

/* ---------- Antet de pas (cerc roșu cu număr + titlu) ---------- */
.pas {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.25rem 0 0.5rem;
}
.pas-nr {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: var(--accent);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 0 0 4px var(--accent-soft);
}
.pas-titlu {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.015em;
}

/* ---------- Stare goală (când nu e ales niciun material) ---------- */
.gol {
    text-align: center;
    padding: 2.25rem 1.25rem;
    border: 1px dashed var(--border-hover);
    border-radius: 14px;
    background: var(--surface);
}
.gol-titlu {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.4rem;
}
.gol-text {
    max-width: 34rem;
    margin: 0 auto 1rem;
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.55;
}
.gol-indiciu {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-weight: 600;
    font-size: 0.82rem;
}

/* ---------- Subsol ---------- */
.subsol {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.78rem;
    line-height: 1.6;
}

/* ---------- Carduri (containere cu bordură) ----------
   Doar rotunjire și culoarea bordurii: nu punem fundal sau umbră aici, fiindcă
   același element învelește și blocurile fără bordură. */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: var(--raza);
    border-color: var(--border) !important;
    transition: border-color 0.2s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover > div {
    border-color: var(--border-hover) !important;
}

/* ---------- Tab-uri ---------- */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 2px;
    border-bottom: 1px solid var(--border);
}
[data-testid="stTabs"] button[role="tab"] {
    font-weight: 600;
    color: var(--muted);
    padding: 0.6rem 0.9rem;
    border-radius: 8px 8px 0 0;
    transition: color 0.15s ease, background-color 0.15s ease;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #E4E4E8;
    background-color: rgba(255, 255, 255, 0.04);
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--accent);
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: var(--accent);
    height: 3px;
    border-radius: 3px 3px 0 0;
    transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1),
        width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stTabs"] [data-baseweb="tab-border"] {
    background-color: var(--border);
}

/* ---------- Butoane ---------- */
button[data-testid^="stBaseButton-"],
button[data-testid^="baseButton-"] {
    border-radius: 10px !important;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.2s ease,
        background-color 0.15s ease, border-color 0.15s ease,
        color 0.15s ease, filter 0.15s ease;
}
button[data-testid^="stBaseButton-"]:hover,
button[data-testid^="baseButton-"]:hover {
    transform: translateY(-1px);
}
button[data-testid^="stBaseButton-"]:active,
button[data-testid^="baseButton-"]:active {
    transform: translateY(0) scale(0.985);
}
button[data-testid^="stBaseButton-"]:disabled,
button[data-testid^="baseButton-"]:disabled {
    transform: none;
    opacity: 0.5;
}
button[data-testid^="stBaseButton-"]:focus-visible,
button[data-testid^="baseButton-"]:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

/* Butoane secundare: discrete, cu bordură; roșu la hover */
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-secondaryFormSubmit"],
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-secondaryFormSubmit"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
}
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-secondaryFormSubmit"]:hover {
    border-color: rgba(229, 56, 59, 0.65);
    background-color: var(--accent-soft);
}

/* Butoane principale: roșu plin, cu strălucire fină */
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"],
button[kind="primary"] {
    background: linear-gradient(180deg, #EA4A4D 0%, #D42F32 100%) !important;
    border: 1px solid #C92F32 !important;
    color: #FFFFFF !important;
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.18) inset,
        0 4px 14px var(--accent-glow);
}
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover,
button[kind="primary"]:hover {
    filter: brightness(1.07);
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.18) inset,
        0 8px 22px var(--accent-glow);
}

/* ---------- Câmpuri de text, liste, încărcare fișier ---------- */
[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"] {
    border-radius: 10px !important;
    border-color: var(--border) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
[data-baseweb="select"] > div:hover,
[data-baseweb="input"]:hover,
[data-baseweb="textarea"]:hover {
    border-color: var(--border-hover) !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}

[data-testid="stFileUploaderDropzone"] {
    border: 1.5px dashed var(--border-hover) !important;
    border-radius: var(--raza) !important;
    background: var(--surface) !important;
    transition: border-color 0.2s ease, background-color 0.2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--accent) !important;
    background: var(--accent-soft) !important;
}

[data-testid="stForm"] {
    border-radius: 14px !important;
    border-color: var(--border) !important;
}

/* ---------- Secțiuni pliabile, conversație, meniu de profil ---------- */
[data-testid="stExpander"] details {
    border: 1px solid var(--border) !important;
    border-radius: var(--raza) !important;
    background: var(--surface);
}
[data-testid="stExpander"] summary:hover {
    color: var(--accent);
}
[data-testid="stExpanderDetails"] {
    animation: aparitie 0.25s ease both;
}

[data-testid="stChatMessage"] {
    border: 1px solid var(--border);
    border-radius: var(--raza);
    background: var(--surface);
}

[data-testid="stPopoverBody"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

/* ---------- Scoruri, progres, mesaje ---------- */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--raza);
    padding: 0.8rem 1rem;
    transition: background-color 0.15s ease;
}
[data-testid="stMetric"]:hover {
    background: var(--accent-soft);
}
[data-testid="stMetricValue"] {
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    color: var(--muted);
}

[data-testid="stProgress"] [role="progressbar"],
[data-testid="stProgress"] [role="progressbar"] div {
    border-radius: 999px;
    transition: width 0.5s ease;
}

[data-testid="stAlert"] {
    border-radius: var(--raza);
    border: 1px solid rgba(255, 255, 255, 0.07);
    animation: aparitie 0.3s ease both;
}
/* Mesajele de informare, în gri neutru (nu albastru), ca să rămână în paleta
   negru + roșu. Dacă versiunea de Streamlit nu are aceste marcaje, regula pur
   și simplu nu se aplică. */
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
    background: rgba(255, 255, 255, 0.04);
    border-left: 3px solid #5A5A63;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]),
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) p {
    color: #D9D9DE;
}

/* ---------- Bară de derulare ---------- */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #2A2A30;
    border-radius: 10px;
    border: 2px solid transparent;
    background-clip: content-box;
}
::-webkit-scrollbar-thumb:hover {
    background: #3C3C45;
    background-clip: content-box;
}

/* ---------- Butonul de profil ----------
   Tras spre marginea stângă a ecranului. Marginea nu poate deveni pozitivă
   (min cu 0), ca să nu sară în dreapta pe ferestre înguste. */
div[class*="st-key-profil_fixat"] {
    width: fit-content;
    margin-left: min(0px, calc((var(--latime) - 100vw) / 2 + 1rem));
    margin-bottom: 0.25rem;
}
div[class*="st-key-profil_fixat"] button {
    border: 1px solid var(--border) !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 10px !important;
    padding: 0.45rem 0.9rem !important;
    font-weight: 600;
}
div[class*="st-key-profil_fixat"] button span[data-testid="stIconMaterial"],
div[class*="st-key-profil_fixat"] button svg {
    color: var(--accent) !important;
}
div[class*="st-key-profil_fixat"] button:hover {
    border-color: var(--accent) !important;
    background-color: var(--accent-soft) !important;
    box-shadow: 0 2px 10px rgba(229, 56, 59, 0.2);
}

/* ---------- Animații ---------- */
@keyframes aparitie {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

/* ---------- Ecrane mici ---------- */
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"], .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero-titlu { font-size: 1.7rem; }
    .hero-marca { height: 38px; }
    .pas-titlu { font-size: 1.2rem; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; }
    div[class*="st-key-profil_fixat"] {
        margin-left: 0;
    }
}
</style>
"""
