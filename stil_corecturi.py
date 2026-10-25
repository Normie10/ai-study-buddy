"""Corecturi mici de stil, adăugate peste CSS_UI din stil_ui.py."""

from stil_ui import CSS_UI as _CSS_UI_BAZA

_CSS_CORECTURI = """
<style>
/* Bara de sus a Streamlit acoperea butonul de profil. O ascundem complet,
   împreună cu linia colorată de deasupra ei. */
[data-testid="stHeader"],
[data-testid="stDecoration"] {
    display: none !important;
}
/* Fără bară, conținutul poate începe mai sus, iar butonul de profil urcă. */
[data-testid="stMainBlockContainer"], .block-container {
    padding-top: 1.5rem !important;
}
/* Butonul de profil, deasupra oricărui alt strat */
div[class*="st-key-profil_fixat"] {
    position: relative;
    z-index: 1000;
}
</style>
"""

CSS_UI = _CSS_UI_BAZA + _CSS_CORECTURI
