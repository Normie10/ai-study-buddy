"""Corecturi mici de stil, adăugate peste CSS_UI din stil_ui.py."""

from stil_ui import CSS_UI as _CSS_UI_BAZA

_CSS_CORECTURI = """
<style>
/* Bara de sus a Streamlit (aprox. 3,75 rem) acoperea partea de sus a
   butonului de profil și prindea click-urile. Mutăm tot conținutul paginii
   mai jos, sub bară, ca butonul să nu mai fie acoperit. */
[data-testid="stMainBlockContainer"], .block-container {
    padding-top: 4.5rem !important;
}
/* Butonul de profil, deasupra oricărui alt strat */
div[class*="st-key-profil_fixat"] {
    position: relative;
    z-index: 1000;
}
</style>
"""

CSS_UI = _CSS_UI_BAZA + _CSS_CORECTURI
