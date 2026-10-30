"""Stil în plus pentru pagina principală (antetul) și pentru pagina de
abonamente: animații discrete, panou cu lumină roșie, carduri mai aerisite.
Se aplică peste stilurile existente, fără să le schimbe."""

CSS_ACASA = """
<style>
@keyframes urca {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: none; }
}
@keyframes puls_bara {
    0%, 100% { box-shadow: 0 0 14px rgba(229, 56, 59, 0.35); }
    50% { box-shadow: 0 0 26px rgba(229, 56, 59, 0.65); }
}
@keyframes inel {
    0% { box-shadow: 0 0 0 0 rgba(229, 56, 59, 0.45); }
    100% { box-shadow: 0 0 0 10px rgba(229, 56, 59, 0); }
}

/* ---------- Antetul paginii principale (doar .hero-nou) ---------- */
.hero.hero-nou {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.25rem;
    border: 1px solid var(--border);
    border-radius: 18px;
    background: linear-gradient(
        135deg, rgba(229, 56, 59, 0.07), rgba(255, 255, 255, 0.015) 55%
    );
}
.hero.hero-nou::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: -45%;
    left: -10%;
    width: 60%;
    height: 190%;
    background: radial-gradient(closest-side, rgba(229, 56, 59, 0.15), transparent);
    pointer-events: none;
}
.hero.hero-nou .hero-marca {
    height: 74px;
    animation: puls_bara 4.5s ease-in-out infinite;
}
.hero.hero-nou .hero-titlu {
    font-size: 2.6rem;
    color: #F2F2F4;
}
.hero.hero-nou .hero-sub {
    font-size: 1.02rem;
    max-width: 38rem;
}
.hero.hero-nou .hero-continut > * {
    animation: urca 0.6s ease backwards;
}
.hero.hero-nou .hero-continut > *:nth-child(2) { animation-delay: 0.08s; }
.hero.hero-nou .hero-continut > *:nth-child(3) { animation-delay: 0.16s; }
.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
}
.hero-chip {
    padding: 0.3rem 0.85rem;
    border: 1px solid var(--border-hover);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.03);
    color: var(--muted);
    font-size: 0.82rem;
    font-weight: 600;
}
.hero-chip::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 6px;
    margin-right: 0.5rem;
    border-radius: 50%;
    background: var(--accent);
    vertical-align: middle;
}

/* ---------- Pașii, starea goală, zona de încărcare ---------- */
.pas-nr {
    animation: inel 2.4s ease-out 1;
}
.gol {
    background: radial-gradient(
            ellipse at top, rgba(229, 56, 59, 0.08), transparent 70%
        ),
        var(--surface);
    animation: urca 0.5s ease backwards;
}
.gol-indiciu {
    animation: inel 2.6s ease-out 2;
}
[data-testid="stFileUploaderDropzone"] {
    padding: 1.4rem 1.2rem !important;
}
[data-testid="stExpander"] details {
    transition: border-color 0.2s ease;
}
[data-testid="stExpander"] details:hover {
    border-color: rgba(229, 56, 59, 0.45) !important;
}

@media (max-width: 640px) {
    .hero.hero-nou { padding: 1.1rem 1rem; }
    .hero.hero-nou .hero-titlu { font-size: 1.9rem; }
    .hero.hero-nou .hero-marca { height: 56px; }
}
</style>
"""

CSS_ABONAMENTE_EXTRA = """
<style>
@keyframes urca {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: none; }
}
.abon-antet, .abon-prototip {
    animation: urca 0.5s ease backwards;
}
.abon-titlu {
    font-size: 2.2rem;
}
.planuri .plan {
    animation: urca 0.55s ease backwards;
    transition: transform 0.25s ease, border-color 0.2s ease,
        box-shadow 0.25s ease;
}
.planuri .plan:nth-child(2) {
    animation-delay: 0.1s;
}
.planuri .plan:hover {
    transform: translateY(-4px);
}
.plan-premium {
    box-shadow: 0 14px 40px rgba(229, 56, 59, 0.16);
}
.plan-premium:hover {
    box-shadow: 0 18px 48px rgba(229, 56, 59, 0.26);
}
.plan-nume {
    font-size: 1.15rem;
    letter-spacing: -0.01em;
}
.plan-suma {
    font-size: 2.7rem;
}
.plan-lista li {
    transition: transform 0.15s ease;
}
.plan-lista li:hover {
    transform: translateX(3px);
}
</style>
"""
