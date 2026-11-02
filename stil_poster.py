"""Aranjamentul paginii Acasă după poza de referință: bun venit cu robotul,
zona de încărcare, cardurile, apoi activitate / progres / Premium.
Se adaugă la tema din stil_tema.py și suprascrie regulile Acasă de acolo."""

CSS_POSTER = """
/* spații mai mici între blocurile paginii Acasă */
[data-testid="stMainBlockContainer"]:has(.aca-marker) > [data-testid="stVerticalBlock"] {
    gap: 1.2rem;
}

/* ----- bun venit: titlu pe două rânduri, robotul în dreapta ----- */
div[class*="st-key-aca_hero"] {
    z-index: 0;
    min-height: 12.2rem;
    margin-bottom: -1.7rem;
    background: radial-gradient(closest-side at 78% 45%, var(--glow), transparent);
}
.aca-hero-text { max-width: 55% !important; min-height: 0 !important; padding-top: 0.6rem; }
.aca-titlu { font-size: clamp(1.9rem, 3.1vw, 2.9rem); line-height: 1.08; }
.aca-sub { font-size: 1rem; }
.aca-robot { right: 9% !important; top: 0 !important; width: 215px !important; }

/* ----- zona de încărcare: compactă, stă peste marginea de jos a robotului ----- */
div[class*="st-key-aca_upload"] {
    position: relative;
    z-index: 1;
    padding: 1.3rem 1.5rem 1.2rem;
    border: 2px dashed rgba(139, 92, 246, 0.50);
    border-radius: 20px;
    background: var(--camp-bg);
    box-shadow: var(--sombra);
    text-align: center;
    animation: urca 0.5s ease 0.05s backwards;
}
.aca-up { display: flex; flex-direction: column; align-items: center; gap: 0.25rem; margin-bottom: 0.6rem; }
.aca-up-ic {
    display: inline-grid;
    place-items: center;
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: rgba(139, 92, 246, 0.14);
}
.aca-up-t { margin-top: 0.2rem; font-size: 1.3rem; font-weight: 800; letter-spacing: -0.02em; }
.aca-up-s { color: var(--muted); font-size: 0.88rem; }
div[class*="st-key-aca_upload"] button {
    min-height: 2.8rem;
    border-radius: 999px !important;
    font-size: 1rem;
}

/* ----- cardurile: mai joase, cu săgeată rotundă în colț ----- */
div[class*="st-key-aca_card_"] {
    min-height: 7.4rem;
    padding: 0.85rem 0.85rem 1rem;
}
div[class*="st-key-aca_card_"]::after {
    content: "→";
    position: absolute;
    right: 0.75rem;
    bottom: 0.7rem;
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
.aca-ct { margin-top: 0.5rem; }
.aca-cd { min-height: 1.4em; padding-right: 2.2rem; }

/* ----- rândul de jos: activitate, progres, Premium (aceeași înălțime) ----- */
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_progres"],
div[class*="st-key-aca_premium"] { min-height: 19.5rem; }

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

/* bannerul Premium: titlul pe toată lățimea, lista mai îngustă, robotul jos în dreapta */
div[class*="st-key-aca_premium"] { padding: 1.3rem 1.4rem; }
.aca-pb { max-width: 100% !important; }
.aca-pb-t { font-size: 1.1rem; }
.aca-pb-s { font-size: 0.85rem; }
.aca-pb-l { max-width: 62%; }
.aca-pb-l li { font-size: 0.82rem; }
.aca-prem-robot { width: 165px !important; right: 0.3rem !important; }

@media (max-width: 760px) {
    div[class*="st-key-aca_hero"] { min-height: 0; margin-bottom: 0; }
    .aca-hero-text { max-width: 100% !important; }
    .aca-pg { flex-wrap: wrap; }
    .aca-pb-l { max-width: 100%; }
}
"""
