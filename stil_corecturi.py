"""Corecturi mici de stil, adăugate peste CSS_UI din stil_ui.py."""

from stil_ui import CSS_UI as _CSS_UI_BAZA

_CSS_CORECTURI = """
<style>
/* Bara de sus a Streamlit e transparentă, dar prindea click-urile din colțul
   stânga-sus, deasupra butonului de profil. Ea nu mai prinde click-uri; meniul
   ei (Deploy, trei puncte) rămâne funcțional. */
[data-testid="stHeader"] {
    pointer-events: none;
}
[data-testid="stHeader"] [data-testid="stToolbar"],
[data-testid="stHeader"] [data-testid="stToolbar"] * {
    pointer-events: auto;
}
/* Butonul de profil, deasupra oricărui alt strat */
div[class*="st-key-profil_fixat"] {
    position: relative;
    z-index: 1000;
}
</style>
"""

CSS_UI = _CSS_UI_BAZA + _CSS_CORECTURI
