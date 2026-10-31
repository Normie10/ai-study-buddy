"""Tema violet închis: fundal aproape negru, accente violet și magenta discrete,
meniu lateral cu categorii pliabile, pagina Acasă. Se încarcă după celelalte
stiluri și le suprascrie."""

CSS_TEMA = """
<style>
@keyframes urca {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: none; }
}

/* ---------- Culorile temei ---------- */
:root {
    --accent: #8B5CF6;
    --accent-soft: rgba(139, 92, 246, 0.12);
    --accent-glow: rgba(139, 92, 246, 0.22);
    --border: #251F42;
    --border-hover: #3B3268;
    --surface: rgba(255, 255, 255, 0.025);
    --muted: #9D9AB6;
}
::selection { background: rgba(139, 92, 246, 0.35); }

[data-testid="stApp"] {
    background:
        radial-gradient(900px 480px at 85% -8%, rgba(139, 92, 246, 0.10), transparent 60%),
        #08070F !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent !important;
}
[data-testid="stSidebar"] {
    background: #0B0914 !important;
    border-right: 1px solid var(--border);
}
/* Bara de sus rămâne (are butonul care deschide meniul pe telefon), dar fără
   uneltele Streamlit din dreapta */
[data-testid="stHeader"] {
    display: flex !important;
    background: transparent !important;
}
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background-color: #100D20 !important;
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
    width: 44px;
    height: 44px;
    mix-blend-mode: screen;
}
.brand-nume {
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.brand-nume b { color: #C4B5FD; }

div[class*="st-key-profil_lateral"] [data-testid="stPopover"],
div[class*="st-key-profil_lateral"] button {
    width: 100% !important;
    justify-content: flex-start !important;
}

/* spații mici între elementele meniului */
div[class*="st-key-meniu_lateral"],
div[class*="st-key-meniu_lateral"] [data-testid="stVerticalBlock"] {
    gap: 0.2rem !important;
}
div[class*="st-key-meniu_lateral"] {
    margin-top: 0.8rem;
}

/* butoanele din meniu: aliniate la stânga, plate */
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
    color: #CFCCE6 !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-secondary"]:hover,
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-secondary"]:hover {
    background: rgba(139, 92, 246, 0.10) !important;
    border-color: transparent !important;
    color: #FFFFFF !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-primary"],
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-primary"] {
    background: rgba(139, 92, 246, 0.18) !important;
    border: 1px solid rgba(139, 92, 246, 0.45) !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}

/* categoriile pliabile */
[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border: 0 !important;
    background: transparent !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    padding: 0.55rem 0.7rem;
    border-radius: 10px;
    font-weight: 700;
    color: #E6E3F7;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background: rgba(139, 92, 246, 0.10);
    color: #FFFFFF;
}
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
    padding: 0.2rem 0 0.4rem 0.5rem;
}

div[class*="st-key-meniu_premium"] {
    margin-top: 1.2rem;
    padding: 0.8rem;
    border: 1px solid var(--border-hover);
    border-radius: 12px;
    background: rgba(139, 92, 246, 0.07);
}
.meniu-prem-t {
    margin-bottom: 0.3rem;
    font-size: 0.92rem;
    font-weight: 700;
}

/* ---------- Pagini ---------- */
.pagina-titlu {
    margin: 0.2rem 0 0.2rem;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    animation: urca 0.4s ease backwards;
}
.pagina-sub {
    margin-bottom: 0.8rem;
    color: var(--muted);
}
.material-activ {
    padding: 0.3rem 0;
    color: var(--muted);
    font-size: 0.88rem;
}

/* ---------- Pagina Acasă ---------- */
.aca-marker { display: none; }
[data-testid="stMainBlockContainer"]:has(.aca-marker) {
    max-width: 1080px !important;
}
[data-testid="stMainBlockContainer"]:has(.aca-marker) > [data-testid="stVerticalBlock"] {
    gap: 1.5rem;
}

div[class*="st-key-aca_hero"] {
    position: relative;
    overflow: hidden;
    padding: 2rem 2.2rem 1.8rem;
    border: 1px solid var(--border-hover);
    border-radius: 20px;
    background:
        radial-gradient(closest-side at 88% 45%, rgba(217, 70, 239, 0.12), transparent 55%),
        linear-gradient(115deg, #1A1337 0%, #110D26 58%, #0D0A1C 100%);
    animation: urca 0.5s ease backwards;
}
.aca-hero-text { max-width: 62%; }
.aca-titlu {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.aca-nume { color: #C4B5FD; }
.aca-sub {
    margin-top: 0.5rem;
    color: #CFCCE6;
    font-size: 1.02rem;
}
.aca-material {
    margin: 0.7rem 0 0.3rem;
    color: var(--muted);
    font-size: 0.88rem;
}
.aca-logo {
    position: absolute;
    right: 1.8rem;
    top: 50%;
    height: 190px;
    width: auto;
    transform: translateY(-50%);
    mix-blend-mode: screen;
    pointer-events: none;
}
div[class*="st-key-aca_hero"] button {
    padding: 0.7rem 1rem !important;
    min-height: 2.9rem;
    border-radius: 12px !important;
}
div[class*="st-key-aca_hero"] button[data-testid="stBaseButton-secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--border-hover) !important;
    color: #FFFFFF !important;
}

div[class*="st-key-aca_progres"],
div[class*="st-key-aca_recent"] {
    padding: 1.4rem 1.5rem;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.025);
    animation: urca 0.5s ease 0.08s backwards;
}
div[class*="st-key-aca_premium"] {
    padding: 1.1rem 1.5rem;
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.10), rgba(217, 70, 239, 0.04));
    animation: urca 0.5s ease 0.16s backwards;
}
.aca-card-titlu { font-size: 1.15rem; font-weight: 700; }
.aca-prem-t { font-size: 1.05rem; font-weight: 700; }
.aca-prem-d { margin-top: 0.15rem; color: var(--muted); font-size: 0.9rem; }

.aca-prog {
    display: flex;
    align-items: center;
    gap: 1.4rem;
    margin-top: 0.9rem;
}
.aca-inel {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 104px;
    height: 104px;
    border-radius: 50%;
    background: conic-gradient(
        #8B5CF6 0, #D946EF calc(var(--p) * 1%), rgba(139, 92, 246, 0.14) 0
    );
}
.aca-inel-in {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #0E0B1D;
}
.aca-inel-in b { font-size: 1.45rem; line-height: 1.1; }
.aca-inel-in span { color: var(--muted); font-size: 0.68rem; }
.aca-rows { flex: 1; margin: 0; padding: 0; list-style: none; }
.aca-rows li {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.3rem 0;
    font-size: 0.9rem;
}
.aca-rows li span { flex: 1; }
.aca-pct { width: 9px; height: 9px; border-radius: 50%; }
.aca-pct.p1 { background: #8B5CF6; }
.aca-pct.p2 { background: #D946EF; }
.aca-pct.p3 { background: #6B7280; }
.aca-mesaj { margin-top: 0.9rem; color: var(--muted); font-size: 0.88rem; }

.aca-rec { margin: 0.6rem 0 0; padding: 0; list-style: none; }
.aca-rec li {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.92rem;
}
.aca-rec li:last-child { border-bottom: 0; }
.aca-rec li span { flex: 1; }
.aca-rec li em { color: var(--muted); font-size: 0.8rem; font-style: normal; }
.aca-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #8B5CF6;
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
    color: #C4B5FD !important;
}

/* ---------- Ecrane mici ---------- */
@media (max-width: 760px) {
    .aca-hero-text { max-width: 100%; }
    .aca-logo { display: none; }
    .aca-titlu { font-size: 1.8rem; }
    div[class*="st-key-aca_hero"] { padding: 1.4rem 1.2rem; }
    .aca-prog { flex-direction: column; align-items: flex-start; }
}
</style>
"""
