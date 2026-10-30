"""Antetul paginii principale: bara roșie, titlul, subtitlul și trei pastile."""

import html

from limbi import t


def hero_acasa():
    """Totul pe un singur rând, fără linii goale, altfel Markdown strică HTML-ul."""
    pastile = "".join(
        f'<span class="hero-chip">{html.escape(t(cheie))}</span>'
        for cheie in ("acasa.pastila1", "acasa.pastila2", "acasa.pastila3")
    )
    return (
        '<div class="hero hero-nou"><div class="hero-marca"></div>'
        '<div class="hero-continut">'
        f'<div class="hero-titlu">{html.escape(t("hero.titlu"))}</div>'
        f'<div class="hero-sub">{html.escape(t("hero.sub"))}</div>'
        f'<div class="hero-chips">{pastile}</div>'
        "</div></div>"
    )
