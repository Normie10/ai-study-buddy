"""Corecturi pentru pagina Acasă (se adaugă la sfârșitul lui CSS_TEMA)."""

CSS_CORECTURI_ACASA = """
<style>
/* lumina din spatele robotului: se stinge înainte de marginea casetei */
div[class*="st-key-aca_hero"] {
    background: radial-gradient(
        closest-side at 82% 38%, rgba(139, 92, 246, 0.2), transparent
    ) !important;
}
/* cardurile mici au aceeași înălțime */
.aca-cd { min-height: 2.7em; }
/* robot mai mic în meniu */
.meniu-robot { max-width: 150px !important; }
/* Activitate recentă și Premium se termină la aceeași înălțime */
div[class*="st-key-aca_recent"],
div[class*="st-key-aca_premium"] { min-height: 21.5rem; }
/* robotul din banner nu mai intră sub carduri */
@media (min-width: 761px) {
    .aca-hero-text { min-height: 12.5rem !important; }
    .aca-robot { width: 240px !important; top: -6px !important; }
}
</style>
"""
