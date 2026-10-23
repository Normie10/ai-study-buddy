"""Obiectivul zilnic și seria de zile: un card sub antet, care arată câte
activități ai terminat azi și câte zile la rând ai învățat. Datele vin din
rezultatele deja salvate pe cont (nu e nevoie de un tabel nou)."""

import html
from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from baza_date import (
    date_progres,
    obiectiv_zilnic,
    seteaza_obiectiv,
    utilizator_curent,
)

FUS_ORAR = "Europe/Bucharest"

CSS_OBIECTIV = """
<style>
.obiectiv {
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 0.75rem;
    margin: 0.25rem 0 0.75rem;
    animation: aparitie 0.4s ease both;
}
.ob-bloc {
    padding: 0.9rem 1.1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--raza);
    transition: border-color 0.2s ease;
}
.ob-bloc:hover {
    border-color: var(--border-hover);
}
.ob-eticheta {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.ob-valoare {
    margin-top: 0.35rem;
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.15;
}
.ob-valoare span {
    margin-left: 0.4rem;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0;
    color: var(--muted);
}
.ob-bara {
    margin-top: 0.6rem;
    height: 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
}
.ob-umplere {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #F0494C, #E5383B);
    box-shadow: 0 0 12px var(--accent-glow);
    animation: umple 0.8s ease both;
}
@keyframes umple {
    from { width: 0; }
}
.ob-nota {
    margin-top: 0.55rem;
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.4;
}
.ob-saptamana {
    display: flex;
    gap: 0.35rem;
    margin-top: 0.6rem;
}
.ob-zi {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 1px solid var(--border-hover);
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 700;
}
.ob-zi-activa {
    background: var(--accent);
    border-color: var(--accent);
    color: #FFFFFF;
}
.ob-zi-azi {
    box-shadow: 0 0 0 3px var(--accent-soft);
}
/* Iconițe desenate din CSS (nu sunt emoji) */
.ob-ico {
    display: inline-block;
    width: 16px;
    height: 16px;
    flex-shrink: 0;
    background: var(--accent);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-size: contain;
    mask-size: contain;
}
.ob-ico-tinta {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Ccircle cx='12' cy='12' r='5'/%3E%3Ccircle cx='12' cy='12' r='1'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='9'/%3E%3Ccircle cx='12' cy='12' r='5'/%3E%3Ccircle cx='12' cy='12' r='1'/%3E%3C/svg%3E");
}
.ob-ico-foc {
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z'/%3E%3C/svg%3E");
}
@media (max-width: 640px) {
    .obiectiv { grid-template-columns: 1fr; }
}
</style>
"""


def _unitate_zile(n):
    """„zi”, „zile” sau „de zile”, după regula din română (20 de zile)."""
    if n == 1:
        return "zi"
    rest = n % 100
    if n == 0 or 1 <= rest < 20:
        return "zile"
    return "de zile"


def _zile_cu_activitate(valori):
    """Din datele salvate (text) face un dicționar: zi -> câte activități."""
    if not valori:
        return Counter()
    try:
        timp = pd.to_datetime(valori, utc=True, format="ISO8601", errors="coerce")
    except (ValueError, TypeError):
        timp = pd.to_datetime(valori, utc=True, errors="coerce")
    timp = timp.dropna().tz_convert(FUS_ORAR)
    return Counter(timp.date)


def _zile_activitate(user_id):
    """Rezumatul se ține minte în sesiune și se reface doar după ce s-a salvat
    un rezultat nou (vezi _tabel_progres_nou din baza_date.py)."""
    cache = st.session_state.get("cache_obiectiv")
    if cache and cache["user"] == user_id:
        return cache["zile"]
    zile = _zile_cu_activitate(date_progres())
    st.session_state["cache_obiectiv"] = {"user": user_id, "zile": zile}
    return zile


def _serii(zile, azi):
    """Întoarce (seria curentă, cea mai lungă serie). Seria curentă rămâne
    vie și dacă azi nu ai făcut încă nimic, dar ai făcut ieri."""
    active = set(zile)
    zi = azi if azi in active else azi - timedelta(days=1)
    curenta = 0
    while zi in active:
        curenta += 1
        zi -= timedelta(days=1)

    cea_mai_lunga, lant, anterioara = 0, 0, None
    for zi in sorted(active):
        if anterioara is not None and zi - anterioara == timedelta(days=1):
            lant += 1
        else:
            lant = 1
        cea_mai_lunga = max(cea_mai_lunga, lant)
        anterioara = zi
    return curenta, cea_mai_lunga


def _saptamana_html(zile, azi):
    bucati = []
    for decalaj in range(6, -1, -1):
        zi = azi - timedelta(days=decalaj)
        clase = "ob-zi"
        if zi in zile:
            clase += " ob-zi-activa"
        if zi == azi:
            clase += " ob-zi-azi"
        bucati.append(f'<span class="{clase}">{"LMMJVSD"[zi.weekday()]}</span>')
    return '<div class="ob-saptamana">' + "".join(bucati) + "</div>"


def _card_html(zile, azi, azi_nr, obiectiv, curenta, record):
    procent = min(100, round(100 * azi_nr / obiectiv))
    if azi_nr >= obiectiv:
        mesaj = "Obiectiv atins azi. Bravo!"
    elif not zile:
        mesaj = "Termină un quiz sau un test ca să începi seria."
    elif azi_nr == 0 and curenta > 0:
        mesaj = "Termină o activitate azi ca să-ți păstrezi seria."
    else:
        ramase = obiectiv - azi_nr
        cuvant = "activitate" if ramase == 1 else "activități"
        mesaj = f"Mai ai {ramase} {cuvant} până la obiectiv."

    # totul pe un singur rând, fără linii goale, altfel Markdown strică HTML-ul
    return "".join(
        [
            '<div class="obiectiv">',
            '<div class="ob-bloc">',
            '<div class="ob-eticheta"><span class="ob-ico ob-ico-tinta"></span>'
            "Obiectiv de azi</div>",
            f'<div class="ob-valoare">{azi_nr} / {obiectiv}'
            "<span>activități terminate</span></div>",
            f'<div class="ob-bara"><div class="ob-umplere" '
            f'style="width:{procent}%"></div></div>',
            f'<div class="ob-nota">{html.escape(mesaj)}</div>',
            "</div>",
            '<div class="ob-bloc">',
            '<div class="ob-eticheta"><span class="ob-ico ob-ico-foc"></span>'
            "Serie</div>",
            f'<div class="ob-valoare">{curenta}'
            f"<span>{_unitate_zile(curenta)} la rând</span></div>",
            _saptamana_html(zile, azi),
            f'<div class="ob-nota">Cea mai lungă serie: '
            f"{record} {_unitate_zile(record)}</div>",
            "</div>",
            "</div>",
        ]
    )


def afiseaza_obiectiv():
    user = utilizator_curent()
    if user is None:
        return  # vizitatorii n-au cont, deci n-au nici obiectiv

    st.markdown(CSS_OBIECTIV, unsafe_allow_html=True)
    try:
        zile = _zile_activitate(user.id)
    except Exception:
        st.caption("Nu am putut încărca obiectivul zilnic acum.")
        return

    azi = datetime.now(ZoneInfo(FUS_ORAR)).date()
    obiectiv = obiectiv_zilnic()
    curenta, record = _serii(zile, azi)
    st.markdown(
        _card_html(zile, azi, zile.get(azi, 0), obiectiv, curenta, record),
        unsafe_allow_html=True,
    )

    with st.popover("Schimbă obiectivul", icon=":material/tune:"):
        nou = st.number_input(
            "Activități pe zi", 1, 10, obiectiv, key="obiectiv_nou"
        )
        st.caption(
            "O activitate este un rezultat salvat: Quiz, Examen, SAT, "
            "Adevărat/Fals sau Completează. Flashcardurile nu se numără."
        )
        if st.button("Salvează obiectivul", key="obiectiv_salveaza", type="primary"):
            st.session_state["obiectiv_doar_sesiune"] = not seteaza_obiectiv(nou)
            st.rerun()
        if st.session_state.get("obiectiv_doar_sesiune"):
            st.warning(
                "Nu am putut salva obiectivul pe cont; e valabil doar cât "
                "ții pagina deschisă."
            )
