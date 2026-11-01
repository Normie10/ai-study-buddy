"""Tema AI Study Buddy, în două moduri: luminos și întunecat.

Culorile de bază (fundal, text, câmpuri, grafice) vin din .streamlit/config.toml
([theme.light] și [theme.dark]). Aici sunt doar stilurile noastre: meniul,
pagina Acasă, cardurile. Modul activ se află cu st.context.theme; dacă nu se
poate afla, se folosește modul întunecat (aspectul de până acum).
Se încarcă ultimul, ca să suprascrie celelalte stiluri."""

import streamlit as st


def mod_curent():
    """'light' sau 'dark'. Dacă Streamlit nu spune, 'dark'."""
    try:
        tema = st.context.theme
        valoare = getattr(tema, "base", None) or getattr(tema, "type", None)
        if valoare in ("light", "dark"):
            return valoare
    except Exception:
        pass
    return "dark"


# ---------- variabilele care diferă între moduri ----------
_VARS_INTUNECAT = """
:root {
    --accent-text: #B58BFF;
    --accent-text-2: #C4B5FD;
    --activ-text: #FFFFFF;
    --camp-bg: #100D20;
    --panou: rgba(255, 255, 255, 0.025);
    --card-sus: 0.18;
    --card-jos: 0.04;
    --glow: rgba(139, 92, 246, 0.14);
    --sombra: none;
    --ok: #3FD58A;
    --bad: #FF6B81;
}
[data-testid="stApp"] { background-color: #08070F !important; }
[data-testid="stSidebar"] { background: #0B0914 !important; }
"""

_VARS_LUMINOS = """
:root {
    --accent-text: #6D3FD8;
    --accent-text-2: #5B34C2;
    --activ-text: #3F1FA8;
    --camp-bg: #FFFFFF;
    --panou: #FFFFFF;
    --card-sus: 0.26;
    --card-jos: 0.12;
    --glow: rgba(139, 92, 246, 0.16);
    --sombra: 0 4px 18px rgba(80, 60, 160, 0.08);
    --ok: #15803D;
    --bad: #DC2626;
}
[data-testid="stApp"] { background-color: #F6F3FF !important; }
[data-testid="stSidebar"] { background: #FBFAFF !important; }
/* robotul din imaginea de referință e făcut pentru fundal închis:
   în modul luminos îl ascundem până avem o variantă luminoasă */
.aca-robot, .meniu-robot { display: none !important; }
.aca-hero-text { max-width: 75% !important; }
"""

# ---------- stilul comun ----------
_BAZA = """
@keyframes urca {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: none; }
}

:root {
    --accent: #8B5CF6;
    --accent-soft: rgba(139, 92, 246, 0.12);
    --border: color-mix(in srgb, currentColor 14%, transparent);
    --border-hover: color-mix(in srgb, currentColor 28%, transparent);
    --muted: color-mix(in srgb, currentColor 62%, transparent);
}
::selection { background: rgba(139, 92, 246, 0.35); }

[data-testid="stApp"] {
    background-image:
        radial-gradient(900px 480px at 85% -8%, var(--glow), transparent 60%) !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent !important;
}
[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
}

/* bara de sus: păstrăm meniul Streamlit (de acolo se schimbă modul) */
[data-testid="stHeader"] {
    display: flex !important;
    background: transparent !important;
}
[data-testid="stToolbar"] {
    display: flex !important;
    visibility: visible !important;
}
[data-testid="stAppDeployButton"],
[data-testid="stStatusWidget"],
[data-testid="stDecoration"] {
    display: none !important;
}

[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background-color: var(--camp-bg) !important;
}

/* ---------- Butoane: plate, fără strălucire ---------- */
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"],
button[kind="primary"] {
    background: #6D4AE0 !important;
    border: 1px solid #7C5CF0 !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover,
button[kind="primary"]:hover {
    background: #7A58EE !important;
    filter: none !important;
    box-shadow: 0 6px 18px rgba(109, 74, 224, 0.28) !important;
}
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-secondaryFormSubmit"]:hover {
    border-color: rgba(139, 92, 246, 0.6) !important;
    background-color: var(--accent-soft) !important;
}

/* ---------- Meniul lateral ---------- */
.brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.2rem 0.2rem 0.8rem;
}
.brand-logo {
    width: 42px;
    height: 42px;
    border-radius: 50%;
}
.brand-nume {
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.brand-nume b { color: var(--accent-text); }

div[class*="st-key-profil_lateral"] [data-testid="stPopover"],
div[class*="st-key-profil_lateral"] button {
    width: 100% !important;
    justify-content: flex-start !important;
}

div[class*="st-key-meniu_lateral"],
div[class*="st-key-meniu_lateral"] [data-testid="stVerticalBlock"] {
    gap: 0.2rem !important;
}
div[class*="st-key-meniu_lateral"] {
    margin-top: 0.8rem;
}
div[class*="st-key-meniu_lateral"] button,
div[class*="st-key-meniu_lateral"] button > div,
div[class*="st-key-meniu_lateral"] button [data-testid="stMarkdownContainer"] {
    justify-content: flex-start !important;
    text-align: left !important;
}
div[class*="st-key-meniu_lateral"] button p {
    text-align: left !important;
}
div[class*="st-key-meniu_lateral"] button {
    padding: 0.5rem 0.8rem !important;
    transform: none !important;
    min-height: 2.5rem;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-secondary"],
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-secondary"]:hover,
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-secondary"]:hover {
    background: rgba(139, 92, 246, 0.10) !important;
    border-color: transparent !important;
    color: var(--accent-text) !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-primary"],
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-primary"] {
    background: rgba(139, 92, 246, 0.18) !important;
    border: 1px solid rgba(139, 92, 246, 0.45) !important;
    color: var(--activ-text) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border: 0 !important;
    background: transparent !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    padding: 0.55rem 0.7rem;
    border-radius: 10px;
    font-weight: 700;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background: rgba(139, 92, 246, 0.10);
    color: var(--accent-text);
}
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
    padding: 0.2rem 0 0.4rem 0.5rem;
}

div[class*="st-key-meniu_premium"] {
    margin-top: 1.2rem;
    padding: 0.85rem;
    border: 1px solid rgba(139, 92, 246, 0.5);
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(109, 74, 224, 0.30), rgba(217, 70, 239, 0.10));
}
.meniu-prem-t { font-size: 0.95rem; font-weight: 700; }
.meniu-prem-d { margin: 0.1rem 0 0.4rem; color: var(--muted); font-size: 0.78rem; }
.meniu-robot {
    display: block;
    width: 100%;
    max-width: 150px;
    margin: 1rem auto 0;
}

/* ---------- Pagini ---------- */
.pagina-titlu {
    margin: 0.2rem 0 0.2rem;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    animation: urca 0.4s ease backwards;
}
.pagina-sub { margin-bottom: 0.8rem; color: var(--muted); }
.material-activ { padding: 0.3rem 0; color: var(--muted); font-size: 0.88rem; }

/* ---------- Pagina Acasă ---------- */
.aca-marker { display: none; }
[data-testid="stMainBlockContainer"]:has(.aca-marker) {
    max-width: 1240px !important;
}
[data-testid="stMainBlockContainer"]:has(.aca-marker) > [data-testid="stVerticalBlock"] {
    gap: 1.6rem;
}

div[data-testid="stHorizontalBlock"]:has(.st-key-aca_progres),
div[data-testid="stHorizontalBlock"]:has(.st-key-aca_recent),
div[data-testid="stHorizontalBlock"]:has(.st-key-aca_stats) {
    align-items: stretch !important;
}
div[class*="st-key-aca_progres"],
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_premium"],
div[class*="st-key-aca_stats"],
div[class*="st-key-aca_obiectiv"] {
    height: 100%;
}
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_premium"] { min-height: 21.5rem; }

.aca-ch { display: flex; align-items: center; gap: 0.6rem; }
.aca-chi { display: inline-flex; }
.aca-card-titlu { font-size: 1.1rem; font-weight: 700; }
.aca-mesaj { margin-top: 0.7rem; color: var(--muted); font-size: 0.86rem; }
.aca-centru { text-align: center; }

/* ----- bun venit + robot ----- */
div[class*="st-key-aca_hero"] {
    position: relative;
    padding: 0.4rem 0 0;
    background: radial-gradient(closest-side at 82% 38%, var(--glow), transparent);
    animation: urca 0.5s ease backwards;
}
.aca-hero-text { max-width: 58%; padding-top: 1.2rem; min-height: 10.5rem; }
.aca-titlu {
    font-size: clamp(1.9rem, 3vw, 2.8rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.aca-nume { color: var(--accent-text); }
.aca-sub {
    margin-top: 0.5rem;
    color: color-mix(in srgb, currentColor 82%, transparent);
    font-size: 1.05rem;
}
.aca-material { margin-top: 0.6rem; color: var(--muted); font-size: 0.88rem; }
.aca-robot {
    position: absolute;
    right: 2%;
    top: -10px;
    width: 250px;
    height: auto;
    pointer-events: none;
    z-index: 0;
}

/* ----- cele 6 carduri ----- */
div[class*="st-key-aca_cards"] {
    position: relative;
    z-index: 2;
    margin-top: 0.4rem;
}
div[class*="st-key-aca_card_"] {
    position: relative;
    min-height: 9.6rem;
    padding: 0.95rem 0.85rem 1.1rem;
    border-radius: 16px;
    border: 1px solid rgba(var(--c), 0.40);
    background: linear-gradient(
        160deg, rgba(var(--c), var(--card-sus)), rgba(var(--c), var(--card-jos)) 80%
    );
    box-shadow: var(--sombra);
    cursor: pointer;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
div[class*="st-key-aca_card_"]:hover {
    transform: translateY(-3px);
    border-color: rgba(var(--c), 0.80);
}
div[class*="st-key-aca_card_"]:has(button:focus-visible) {
    outline: 2px solid #A78BFA;
    outline-offset: 2px;
}
.st-key-aca_card_quiz { --c: 244, 63, 94; }
.st-key-aca_card_examen { --c: 249, 115, 22; }
.st-key-aca_card_sat { --c: 59, 130, 246; }
.st-key-aca_card_carduri { --c: 139, 92, 246; }
.st-key-aca_card_rezumat { --c: 34, 197, 94; }
.st-key-aca_card_intreaba { --c: 168, 85, 247; }
/* butonul invizibil care acoperă tot cardul */
div[class*="st-key-aca_card_"] [data-testid="stElementContainer"]:has(button) {
    position: absolute !important;
    inset: 0;
    z-index: 3;
    margin: 0 !important;
}
div[class*="st-key-aca_card_"] [data-testid="stButton"],
div[class*="st-key-aca_card_"] button {
    display: block;
    width: 100% !important;
    height: 100% !important;
}
div[class*="st-key-aca_card_"] button {
    opacity: 0;
    cursor: pointer;
}
div[class*="st-key-aca_card_"] [data-testid="stMarkdownContainer"] p { margin: 0; }
.aca-ci {
    display: inline-grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
}
.aca-ct { margin-top: 0.7rem; font-weight: 700; font-size: 0.98rem; }
.aca-cd {
    margin-top: 0.15rem;
    min-height: 2.7em;
    color: var(--muted);
    font-size: 0.76rem;
    line-height: 1.35;
}

/* ----- carduri generale ----- */
div[class*="st-key-aca_progres"],
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_stats"],
div[class*="st-key-aca_obiectiv"] {
    padding: 1.4rem 1.5rem;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: var(--panou);
    box-shadow: var(--sombra);
    animation: urca 0.5s ease 0.08s backwards;
}

/* ----- progres: inelul e desenat cu mască, ca să nu depindă de culoarea fundalului ----- */
.aca-inel {
    position: relative;
    display: grid;
    place-items: center;
    width: 150px;
    height: 150px;
    margin: 1.1rem auto 0.4rem;
}
.aca-inel::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(
        #2DD4BF 0, #8B5CF6 calc(var(--p) * 1%), rgba(139, 92, 246, 0.16) 0
    );
    -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 15px), #000 calc(100% - 14px));
    mask: radial-gradient(farthest-side, transparent calc(100% - 15px), #000 calc(100% - 14px));
}
.aca-inel-in {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.aca-inel-in b { font-size: 2rem; line-height: 1.1; }
.aca-inel-in span { color: var(--muted); font-size: 0.74rem; }
div[class*="st-key-aca_progres"] button {
    min-height: 3rem;
    background: rgba(139, 92, 246, 0.14) !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
    color: var(--accent-text-2) !important;
}

/* ----- activitate recentă ----- */
div[class*="st-key-aca_recent"] button {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    color: var(--accent-text) !important;
    justify-content: flex-end !important;
}
.aca-rec { margin: 0.4rem 0 0; padding: 0; list-style: none; }
.aca-rec li {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--border);
}
.aca-rec li:last-child { border-bottom: 0; }
.aca-ri {
    flex-shrink: 0;
    display: inline-grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 50%;
}
.ri-q { background: #6D4AE0; }
.ri-e { background: #1FA35C; }
.ri-d { background: #2F6BEA; }
.aca-rt { flex: 1; display: flex; flex-direction: column; }
.aca-rt b { font-size: 0.95rem; }
.aca-rt small { color: var(--muted); font-size: 0.8rem; }
.aca-rec li em { color: var(--muted); font-size: 0.8rem; font-style: normal; }

/* ----- banner Premium: la fel în ambele moduri (fundal violet, text alb) ----- */
div[class*="st-key-aca_premium"] {
    position: relative;
    overflow: hidden;
    padding: 1.6rem 1.8rem;
    border: 1px solid rgba(168, 85, 247, 0.5);
    border-radius: 20px;
    background:
        radial-gradient(closest-side at 100% 100%, rgba(236, 72, 153, 0.26), transparent 60%),
        linear-gradient(100deg, #1D0D2E 0%, #260F3A 55%, #2A1062 100%);
    animation: urca 0.5s ease 0.12s backwards;
}
div[class*="st-key-aca_premium"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}
div[class*="st-key-aca_premium"] .aca-mesaj { color: rgba(255, 255, 255, 0.6) !important; }
.aca-pb { max-width: 56%; }
.aca-pb-t { display: flex; align-items: center; gap: 0.6rem; font-size: 1.35rem; font-weight: 800; }
.aca-coroana { display: inline-flex; }
.aca-pb-s { margin-top: 0.5rem; color: rgba(255, 255, 255, 0.85); font-size: 0.95rem; }
.aca-pb-l { margin: 0.7rem 0 0.3rem; padding: 0; list-style: none; }
.aca-pb-l li {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.18rem 0;
    font-size: 0.9rem;
}
.aca-pb-l li::before {
    content: "✓";
    display: inline-grid;
    place-items: center;
    flex-shrink: 0;
    width: 17px;
    height: 17px;
    border-radius: 5px;
    background: #7C3AED;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
}
.aca-prem-robot {
    position: absolute;
    right: 0.6rem;
    bottom: 0;
    width: 270px;
    height: auto;
    pointer-events: none;
}
div[class*="st-key-aca_premium"] button {
    min-height: 2.9rem;
    background: linear-gradient(90deg, #7C4DFF, #E040A0) !important;
    border: 0 !important;
    color: #FFFFFF !important;
}

/* ----- statistici ----- */
.aca-grila {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.9rem;
    margin-top: 1rem;
}
.aca-tile {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.9rem 1rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: color-mix(in srgb, currentColor 3%, transparent);
}
.aca-ti {
    flex-shrink: 0;
    display: inline-grid;
    place-items: center;
    width: 46px;
    height: 46px;
    border-radius: 50%;
}
.aca-tl { color: var(--muted); font-size: 0.82rem; }
.aca-tv { margin-top: 0.1rem; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; }
.aca-tr { margin-left: 0.6rem; font-size: 0.78rem; font-weight: 600; }
.aca-tr.sus { color: var(--ok); }
.aca-tr.jos { color: var(--bad); }
.aca-tr.egal { color: var(--muted); }

/* ----- obiectiv de azi ----- */
.aca-ob { display: flex; align-items: center; gap: 1rem; margin: 1rem 0 0.8rem; }
.aca-ob-ic {
    flex-shrink: 0;
    display: inline-grid;
    place-items: center;
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: rgba(139, 92, 246, 0.2);
}
.aca-ob-t { font-weight: 700; }
.aca-bara {
    height: 6px;
    margin-top: 0.5rem;
    border-radius: 999px;
    background: rgba(139, 92, 246, 0.16);
    overflow: hidden;
}
.aca-bara i {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2DD4BF, #8B5CF6);
}

/* ---------- Pagina de abonamente, în culorile temei ---------- */
.planuri .plan.plan-premium {
    border-color: rgba(139, 92, 246, 0.5);
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.14), rgba(139, 92, 246, 0.03));
    box-shadow: 0 12px 32px rgba(109, 74, 224, 0.14);
}
.planuri .plan.plan-premium:hover { border-color: #8B5CF6; }
div.st-key-abon_premium_curent button:disabled {
    border-color: rgba(139, 92, 246, 0.5) !important;
    color: var(--accent-text-2) !important;
}

/* ---------- Ecrane mici ---------- */
@media (min-width: 761px) {
    .aca-hero-text { min-height: 12.5rem; }
    .aca-robot { width: 240px; top: -6px; }
}
@media (max-width: 760px) {
    .aca-hero-text { max-width: 100% !important; min-height: 0; }
    .aca-robot, .aca-prem-robot { display: none; }
    .aca-pb { max-width: 100%; }
    .aca-grila { grid-template-columns: 1fr; }
    div[class*="st-key-aca_cards"] [data-testid="stColumn"],
    div[class*="st-key-aca_cards"] [data-testid="column"] {
        flex: 1 1 calc(50% - 0.6rem) !important;
        min-width: calc(50% - 0.6rem) !important;
    }
}
"""


def css_tema(mod=None):
    """CSS-ul temei pentru modul activ (sau pentru cel dat)."""
    if mod is None:
        mod = mod_curent()
    variabile = _VARS_LUMINOS if mod == "light" else _VARS_INTUNECAT
    return "<style>" + variabile + _BAZA + "</style>"


# păstrat ca să nu se strice importurile vechi (varianta întunecată)
CSS_TEMA = css_tema("dark")
