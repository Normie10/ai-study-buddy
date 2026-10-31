"""Tema violet (după modelul ales): fundal indigo, meniu lateral, pagina Acasă.
Se încarcă după celelalte stiluri și le suprascrie."""

CSS_TEMA = """
<style>
@keyframes urca {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: none; }
}
@keyframes plutire {
    0%, 100% { transform: translateY(-50%); }
    50% { transform: translateY(calc(-50% - 8px)); }
}

/* ---------- Culorile temei ---------- */
:root {
    --accent: #A855F7;
    --accent-soft: rgba(168, 85, 247, 0.14);
    --accent-glow: rgba(168, 85, 247, 0.35);
    --border: #2D2468;
    --border-hover: #4A3CB0;
    --surface: rgba(139, 92, 246, 0.07);
    --muted: #A9A4CC;
}
::selection { background: rgba(168, 85, 247, 0.4); }

[data-testid="stApp"] {
    background:
        radial-gradient(1200px 600px at 78% -10%, rgba(139, 92, 246, 0.22), transparent 60%),
        radial-gradient(900px 500px at 5% 105%, rgba(236, 72, 153, 0.10), transparent 60%),
        #0A0620 !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent !important;
}
[data-testid="stSidebar"] {
    background: #0D0828 !important;
    border-right: 1px solid var(--border);
}
/* Bara de sus rămâne vizibilă, ca să poți redeschide meniul pe telefon */
[data-testid="stHeader"] {
    display: flex !important;
    background: transparent !important;
}

/* Câmpuri */
[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background-color: #150F3A !important;
}

/* ---------- Butoane ---------- */
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"],
button[data-testid="baseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"],
button[kind="primary"] {
    background: linear-gradient(180deg, #A06BFF 0%, #7C3AED 100%) !important;
    border: 1px solid #8B5CF6 !important;
    color: #FFFFFF !important;
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.2) inset,
        0 4px 14px rgba(124, 58, 237, 0.4) !important;
}
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover,
button[kind="primary"]:hover {
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.2) inset,
        0 8px 22px rgba(124, 58, 237, 0.5) !important;
}
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-secondaryFormSubmit"]:hover {
    border-color: rgba(168, 85, 247, 0.7) !important;
    background-color: var(--accent-soft) !important;
}

/* ---------- Meniul lateral ---------- */
.brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.2rem 0.2rem 0.9rem;
}
.brand-logo {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    mix-blend-mode: screen;
}
.brand-nume {
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.brand-nume b { color: #C084FC; }
.meniu-grup {
    margin: 1rem 0 0.2rem 0.4rem;
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
div[class*="st-key-profil_lateral"] button {
    width: 100%;
}
div[class*="st-key-meniu_lateral"] button {
    justify-content: flex-start !important;
    padding: 0.5rem 0.8rem !important;
    transform: none !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-secondary"],
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
    color: #D9D6F2 !important;
}
div[class*="st-key-meniu_lateral"] button[data-testid="stBaseButton-secondary"]:hover,
div[class*="st-key-meniu_lateral"] button[data-testid="baseButton-secondary"]:hover {
    background: rgba(168, 85, 247, 0.12) !important;
    border-color: rgba(168, 85, 247, 0.3) !important;
}
div[class*="st-key-meniu_premium"] {
    margin-top: 1.2rem;
    padding: 0.9rem;
    border: 1px solid rgba(168, 85, 247, 0.5);
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.5), rgba(236, 72, 153, 0.18));
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
    max-width: 1120px !important;
}
div[class*="st-key-aca_hero"] {
    position: relative;
    overflow: hidden;
    padding: 1.7rem 1.8rem 1.5rem;
    border: 1px solid var(--border-hover);
    border-radius: 20px;
    background: linear-gradient(
        120deg, rgba(124, 58, 237, 0.38), rgba(30, 18, 92, 0.55) 55%,
        rgba(236, 72, 153, 0.16)
    );
    animation: urca 0.6s ease backwards;
}
div[class*="st-key-aca_hero"]::before {
    content: "";
    position: absolute;
    top: -30%;
    right: -5%;
    width: 50%;
    height: 160%;
    background: radial-gradient(closest-side, rgba(236, 72, 153, 0.28), transparent);
    pointer-events: none;
}
.aca-hero-text { max-width: 60%; }
.aca-titlu {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.aca-nume {
    background: linear-gradient(90deg, #C084FC, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.aca-sub {
    margin-top: 0.5rem;
    color: #D9D6F2;
    font-size: 1.02rem;
}
.aca-logo {
    position: absolute;
    right: 2rem;
    top: 50%;
    width: 210px;
    transform: translateY(-50%);
    mix-blend-mode: screen;
    animation: plutire 5s ease-in-out infinite;
    pointer-events: none;
}
div[class*="st-key-aca_hero"] button {
    justify-content: flex-start !important;
    padding: 0.8rem 1rem !important;
    border-radius: 14px !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
}
.st-key-aca_h_quiz button {
    background: rgba(124, 58, 237, 0.4) !important;
    border: 1px solid rgba(168, 85, 247, 0.6) !important;
}
.st-key-aca_h_examen button {
    background: rgba(37, 99, 235, 0.35) !important;
    border: 1px solid rgba(96, 165, 250, 0.55) !important;
}
.st-key-aca_h_sat button {
    background: rgba(13, 148, 136, 0.35) !important;
    border: 1px solid rgba(45, 212, 191, 0.5) !important;
}

div[class*="st-key-aca_progres"],
div[class*="st-key-aca_rapide"],
div[class*="st-key-aca_recent"] {
    padding: 1.2rem;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: linear-gradient(160deg, rgba(60, 36, 140, 0.3), rgba(20, 12, 60, 0.55));
    animation: urca 0.6s ease 0.1s backwards;
}
div[class*="st-key-aca_premium"] {
    padding: 1.3rem;
    border: 1px solid rgba(168, 85, 247, 0.55);
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.55), rgba(236, 72, 153, 0.2));
    box-shadow: 0 14px 40px rgba(124, 58, 237, 0.2);
    animation: urca 0.6s ease 0.2s backwards;
}
.aca-card-titlu { font-size: 1.2rem; font-weight: 700; }
.aca-prem-t { font-size: 1.25rem; font-weight: 800; }
.aca-prem-d { margin: 0.3rem 0 0.4rem; color: #E4E0FA; font-size: 0.92rem; }

.aca-prog { display: flex; align-items: center; gap: 1.4rem; margin-top: 0.4rem; }
.aca-inel {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: conic-gradient(
        #A855F7 0, #EC4899 calc(var(--p) * 1%), rgba(168, 85, 247, 0.16) 0
    );
}
.aca-inel-in {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 118px;
    height: 118px;
    border-radius: 50%;
    background: #100A33;
}
.aca-inel-in b { font-size: 1.9rem; line-height: 1.1; }
.aca-inel-in span { color: var(--muted); font-size: 0.78rem; }
.aca-rows { flex: 1; margin: 0; padding: 0; list-style: none; }
.aca-rows li {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.35rem 0;
    font-size: 0.92rem;
}
.aca-rows li span { flex: 1; }
.aca-pct { width: 10px; height: 10px; border-radius: 50%; }
.aca-pct.p1 { background: #A855F7; }
.aca-pct.p2 { background: #60A5FA; }
.aca-pct.p3 { background: #2DD4BF; }
.aca-mesaj { margin-top: 0.7rem; color: var(--muted); font-size: 0.88rem; }

div[class*="st-key-aca_q_"] {
    padding: 0.9rem;
    border-radius: 14px;
    border: 1px solid var(--border-hover);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
div[class*="st-key-aca_q_"]:hover { transform: translateY(-3px); }
.st-key-aca_q_quiz { background: linear-gradient(160deg, rgba(124, 58, 237, 0.4), rgba(30, 18, 92, 0.4)); }
.st-key-aca_q_examen { background: linear-gradient(160deg, rgba(37, 99, 235, 0.38), rgba(20, 18, 80, 0.4)); }
.st-key-aca_q_rezumat { background: linear-gradient(160deg, rgba(13, 148, 136, 0.38), rgba(10, 30, 60, 0.4)); }
.st-key-aca_q_intreaba { background: linear-gradient(160deg, rgba(217, 119, 6, 0.38), rgba(50, 20, 40, 0.4)); }
.aca-q-t { font-weight: 700; }
.aca-q-d { margin-bottom: 0.3rem; color: #D9D6F2; font-size: 0.85rem; }

.aca-rec { margin: 0.2rem 0 0; padding: 0; list-style: none; }
.aca-rec li {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.92rem;
}
.aca-rec li:last-child { border-bottom: 0; }
.aca-rec li span { flex: 1; }
.aca-rec li em { color: var(--muted); font-size: 0.8rem; font-style: normal; }
.aca-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #A855F7;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.7);
}

/* ---------- Pagina de abonamente, în culorile temei ---------- */
.planuri .plan.plan-premium {
    border-color: rgba(168, 85, 247, 0.6);
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.18), rgba(139, 92, 246, 0.03));
    box-shadow: 0 14px 40px rgba(124, 58, 237, 0.2);
}
.planuri .plan.plan-premium:hover { border-color: #A855F7; }
div.st-key-abon_premium_curent button:disabled {
    border-color: rgba(168, 85, 247, 0.55) !important;
    color: #C084FC !important;
}

/* ---------- Ecrane mici ---------- */
@media (max-width: 760px) {
    .aca-hero-text { max-width: 100%; }
    .aca-logo { display: none; }
    .aca-titlu { font-size: 1.9rem; }
    .aca-prog { flex-direction: column; align-items: flex-start; }
}
</style>
"""
