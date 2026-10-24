"""Obiectivul zilnic și seria de zile: un card în secțiunea „Progresul meu”,
care arată câte activități ai terminat azi și câte zile la rând ai învățat.
Datele vin din rezultatele deja salvate pe cont (nu e nevoie de un tabel nou)."""

import html
from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st
from limbi import limba_ui, t

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
.ob-unit {
    margin-left: 0.4rem;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0;
    color: var(--muted);
}
.ob-nr {
    display: inline-block;
}
.ob-nota {
    margin-top: 0.55rem;
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.4;
}
.ob-felicitare {
    margin-top: 0.5rem;
    color: var(--accent);
    font-size: 0.9rem;
    font-weight: 700;
    animation: aparitie 0.5s ease 0.4s both;
}

/* ---------- Bara de obiectiv ---------- */
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
/* obiectiv atins: o sclipire lentă peste bară */
.ob-atins .ob-umplere {
    background: linear-gradient(90deg, #E5383B 0%, #FF8A8D 50%, #E5383B 100%);
    background-size: 200% 100%;
    animation: umple 0.8s ease both, sclipire 3s linear infinite;
}
@keyframes sclipire {
    from { background-position: 200% 0; }
    to { background-position: -200% 0; }
}

/* ---------- Seria: flacăra ---------- */
.ob-rand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.35rem;
}
.ob-rand .ob-valoare {
    margin-top: 0;
}
.ob-foc-caseta {
    position: relative;
    display: inline-flex;
    width: 40px;
    height: 40px;
    flex-shrink: 0;
}
.ob-foc-mare {
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, #FF8A8D 0%, #E5383B 55%, #B8282B 100%);
    transform-origin: 50% 90%;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z'/%3E%3C/svg%3E");
}
/* activă: azi ai făcut cel puțin o activitate */
.ob-foc-activ {
    filter: drop-shadow(0 0 7px rgba(229, 56, 59, 0.65));
}
.ob-foc-activ .ob-foc-mare {
    animation: flacara 2.2s ease-in-out infinite;
}
@keyframes flacara {
    0%, 100% { transform: scale(1, 1) rotate(0deg); }
    25% { transform: scale(1.05, 0.97) rotate(-1.5deg); }
    50% { transform: scale(0.97, 1.06) rotate(1deg); }
    75% { transform: scale(1.04, 1.01) rotate(-0.5deg); }
}
/* stinsă: seria e vie, dar azi n-ai făcut încă nimic */
.ob-foc-stins .ob-foc-mare {
    background: #5A5A63;
}
/* fără serie */
.ob-foc-zero .ob-foc-mare {
    background: #3C3C45;
}

/* ---------- Sărbătoare: prima activitate a zilei ---------- */
.ob-sarbatoare .ob-foc-caseta {
    animation: izbucneste 1.1s cubic-bezier(0.2, 0.9, 0.3, 1.3) both;
}
@keyframes izbucneste {
    0% { transform: scale(0.5) rotate(-10deg); opacity: 0; }
    45% { transform: scale(1.35) rotate(4deg); opacity: 1; }
    70% { transform: scale(0.95) rotate(-2deg); }
    100% { transform: scale(1) rotate(0deg); }
}
.ob-sarbatoare .ob-foc-caseta::after {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    opacity: 0;
    animation: inel 1.1s ease-out 0.15s both;
}
@keyframes inel {
    0% { transform: scale(0.6); opacity: 0.9; }
    100% { transform: scale(2.1); opacity: 0; }
}
.ob-sarbatoare .ob-nr {
    animation: pop 0.6s ease 0.25s both;
}
@keyframes pop {
    0% { transform: scale(0.6); opacity: 0; }
    60% { transform: scale(1.25); opacity: 1; }
    100% { transform: scale(1); }
}
.ob-sarbatoare .ob-zi-azi {
    animation: pop 0.6s ease 0.4s both;
}
/* scânteile: invizibile, apar doar la sărbătoare */
.ob-sc {
    position: absolute;
    left: 50%;
    top: 30%;
    width: 5px;
    height: 5px;
    margin-left: -2px;
    border-radius: 50%;
    background: #FF8A8D;
    opacity: 0;
    display: none;
}
.ob-sarbatoare .ob-sc {
    display: block;
    animation-name: scanteie;
    animation-duration: 1s;
    animation-timing-function: ease-out;
    animation-fill-mode: both;
}
@keyframes scanteie {
    0% { transform: translate(0, 0) scale(1); opacity: 1; }
    100% { transform: translate(var(--dx), var(--dy)) scale(0.2); opacity: 0; }
}
.ob-sc1 { --dx: -24px; --dy: -26px; animation-delay: 0.15s; }
.ob-sc2 { --dx: -10px; --dy: -36px; animation-delay: 0.25s; }
.ob-sc3 { --dx: 6px; --dy: -40px; animation-delay: 0.2s; }
.ob-sc4 { --dx: 22px; --dy: -30px; animation-delay: 0.3s; }
.ob-sc5 { --dx: 28px; --dy: -14px; animation-delay: 0.18s; }
.ob-sc6 { --dx: -30px; --dy: -10px; animation-delay: 0.28s; }

/* ---------- Ultimele 7 zile ---------- */
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

/* ---------- Iconița ținței (desenată din CSS, nu e emoji) ---------- */
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


def _e_sarbatoare(user_id, azi, azi_nr):
    """True după ce, în această sesiune, ai făcut prima activitate a zilei.
    Rămâne True până la reîncărcarea paginii, ca să nu pierzi animația dacă
    ai apăsat între timp pe altceva."""
    ultim = st.session_state.get("ob_ultim")
    if (
        ultim
        and ultim[0] == user_id
        and ultim[1] == azi
        and ultim[2] == 0
        and azi_nr >= 1
    ):
        st.session_state["ob_sarbatoare"] = (user_id, azi)
    st.session_state["ob_ultim"] = (user_id, azi, azi_nr)
    return azi_nr >= 1 and st.session_state.get("ob_sarbatoare") == (user_id, azi)


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


def _card_html(zile, azi, azi_nr, obiectiv, curenta, record, sarbatoare):
    procent = min(100, round(100 * azi_nr / obiectiv))
    atins = azi_nr >= obiectiv
    if atins:
        mesaj = "Obiectiv atins azi. Bravo!"
    elif not zile:
        mesaj = "Termină un quiz sau un test ca să începi seria."
    elif azi_nr == 0 and curenta > 0:
        mesaj = "Termină o activitate azi ca să-ți păstrezi seria."
    else:
        ramase = obiectiv - azi_nr
        cuvant = "activitate" if ramase == 1 else "activități"
        mesaj = f"Mai ai {ramase} {cuvant} până la obiectiv."

    if azi_nr >= 1:
        stare_foc = "ob-foc-activ"
    elif curenta > 0:
        stare_foc = "ob-foc-stins"
    else:
        stare_foc = "ob-foc-zero"

    clasa_scop = "ob-bloc ob-atins" if atins else "ob-bloc"
    clasa_serie = "ob-bloc ob-sarbatoare" if sarbatoare else "ob-bloc"
    scanteie = "".join(f'<i class="ob-sc ob-sc{n}"></i>' for n in range(1, 7))

    felicitare = ""
    if sarbatoare:
        text = (
            "Ai început o serie nouă!"
            if curenta == 1
            else "Zi nouă în serie! Continuă și mâine."
        )
        felicitare = f'<div class="ob-felicitare">{text}</div>'

    # totul pe un singur rând, fără linii goale, altfel Markdown strică HTML-ul
    return "".join(
        [
            '<div class="obiectiv">',
            f'<div class="{clasa_scop}">',
            '<div class="ob-eticheta"><span class="ob-ico ob-ico-tinta"></span>'
            "Obiectiv de azi</div>",
            f'<div class="ob-valoare"><span class="ob-nr">{azi_nr} / {obiectiv}</span>'
            '<span class="ob-unit">activități terminate</span></div>',
            f'<div class="ob-bara"><div class="ob-umplere" '
            f'style="width:{procent}%"></div></div>',
            f'<div class="ob-nota">{html.escape(mesaj)}</div>',
            "</div>",
            f'<div class="{clasa_serie}">',
            '<div class="ob-eticheta">Serie</div>',
            '<div class="ob-rand">',
            f'<div class="ob-foc-caseta {stare_foc}"><div class="ob-foc-mare"></div>'
            f"{scanteie}</div>",
            f'<div class="ob-valoare"><span class="ob-nr">{curenta}</span>'
            f'<span class="ob-unit">{_unitate_zile(curenta)} la rând</span></div>',
            "</div>",
            felicitare,
            _saptamana_html(zile, azi),
            f'<div class="ob-nota">Cea mai lungă serie: '
            f"{record} {_unitate_zile(record)}</div>",
            "</div>",
            "</div>",
        ]
    )


def afiseaza_obiectiv(zona):
    """Desenează cardul în containerul `zona` (rezervat în secțiunea
    „Progresul meu” și completat la finalul paginii)."""
    user = utilizator_curent()
    if user is None:
        return  # vizitatorii n-au cont, deci n-au nici obiectiv

    with zona:
        st.markdown(CSS_OBIECTIV, unsafe_allow_html=True)
        try:
            zile = _zile_activitate(user.id)
        except Exception:
            st.caption("Nu am putut încărca obiectivul zilnic acum.")
            return

        azi = datetime.now(ZoneInfo(FUS_ORAR)).date()
        azi_nr = zile.get(azi, 0)
        obiectiv = obiectiv_zilnic()
        curenta, record = _serii(zile, azi)
        sarbatoare = _e_sarbatoare(user.id, azi, azi_nr)
        st.markdown(
            _card_html(zile, azi, azi_nr, obiectiv, curenta, record, sarbatoare),
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
            if st.button(
                "Salvează obiectivul", key="obiectiv_salveaza", type="primary"
            ):
                st.session_state["obiectiv_doar_sesiune"] = not seteaza_obiectiv(nou)
                st.rerun()
            if st.session_state.get("obiectiv_doar_sesiune"):
                st.warning(
                    "Nu am putut salva obiectivul pe cont; e valabil doar cât "
                    "ții pagina deschisă."
                )
