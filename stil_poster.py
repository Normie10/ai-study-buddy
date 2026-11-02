"""Aranjamentul paginii Acasă după poza de referință: bun venit cu robotul,
zona de încărcare, cardurile, apoi activitate / progres / Premium.
Se adaugă la tema din stil_tema.py și suprascrie regulile Acasă de acolo."""

CSS_POSTER = """
/* ----- bun venit: titlu pe două rânduri, robotul în dreapta ----- */
div[class*="st-key-aca_hero"] {
    z-index: 2;
    min-height: 15rem;
    margin-bottom: -2.4rem;
    background: radial-gradient(closest-side at 78% 45%, var(--glow), transparent);
}
.aca-hero-text { max-width: 55% !important; min-height: 0 !important; padding-top: 1.6rem; }
.aca-titlu { font-size: clamp(2.2rem, 4vw, 3.5rem); line-height: 1.08; }
.aca-robot { right: 7% !important; top: 0 !important; width: 250px !important; }

/* ----- zona de încărcare ----- */
div[class*="st-key-aca_upload"] {
    position: relative;
    z-index: 1;
    padding: 2.6rem 1.5rem 1.8rem;
    border: 2px dashed rgba(139, 92, 246, 0.50);
    border-radius: 22px;
    background: var(--panou);
    box-shadow: var(--sombra);
    text-align: center;
    animation: urca 0.5s ease 0.05s backwards;
}
.aca-up { display: flex; flex-direction: column; align-items: center; gap: 0.35rem; margin-bottom: 0.9rem; }
.aca-up-ic {
    display: inline-grid;
    place-items: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(139, 92, 246, 0.14);
}
.aca-up-t { margin-top: 0.4rem; font-size: 1.5rem; font-weight: 800; letter-spacing: -0.02em; }
.aca-up-s { color: var(--muted); font-size: 0.95rem; }
div[class*="st-key-aca_upload"] button {
    min-height: 3.1rem;
    border-radius: 999px !important;
    font-size: 1.02rem;
}

/* ----- cardurile: săgeată rotundă în colț ----- */
div[class*="st-key-aca_card_"]::after {
    content: "→";
    position: absolute;
    right: 0.75rem;
    bottom: 0.75rem;
    display: grid;
    place-items: center;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    border: 1px solid rgba(var(--c), 0.45);
    background: var(--panou);
    color: rgb(var(--c));
    font-size: 0.85rem;
    pointer-events: none;
}
div[class*="st-key-aca_card_"] { min-height: 9.2rem; padding-bottom: 2.6rem; }

/* ----- rândul de jos: activitate, progres, Premium ----- */
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_progres"],
div[class*="st-key-aca_premium"] { min-height: 18.5rem; }

.aca-pg { display: flex; align-items: center; gap: 1.1rem; margin-top: 0.8rem; }
.aca-pg .aca-inel { width: 130px; height: 130px; margin: 0; flex-shrink: 0; }
.aca-pg .aca-inel-in b { font-size: 1.7rem; }
.aca-pg-lista { flex: 1; display: flex; flex-direction: column; gap: 0.75rem; min-width: 0; }
.aca-pg-r { display: flex; align-items: center; gap: 0.7rem; }
.aca-pg-ic {
    flex-shrink: 0;
    display: inline-grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: rgba(139, 92, 246, 0.14);
}
.aca-pg-v { font-weight: 800; font-size: 1.05rem; line-height: 1.15; }
.aca-pg-l { color: var(--muted); font-size: 0.76rem; }
.aca-pg-m { font-size: 0.82rem; line-height: 1.35; font-weight: 600; }
div[class*="st-key-aca_progres"] [data-testid="stButton"] { margin-top: 0.9rem; }

/* bannerul Premium, mai îngust (stă pe același rând cu celelalte două) */
div[class*="st-key-aca_premium"] { padding: 1.3rem 1.4rem; }
.aca-pb { max-width: 62% !important; }
.aca-pb-t { font-size: 1.1rem; }
.aca-pb-s { font-size: 0.85rem; }
.aca-pb-l li { font-size: 0.82rem; }
.aca-prem-robot { width: 165px !important; right: 0.3rem !important; }

@media (max-width: 760px) {
    div[class*="st-key-aca_hero"] { min-height: 0; margin-bottom: 0; }
    .aca-hero-text { max-width: 100% !important; }
    .aca-pg { flex-wrap: wrap; }
    .aca-pb { max-width: 100% !important; }
}
"""
