"""Pagina Acasă, aranjată ca în modelul ales: bun venit cu robotul, zona de
încărcare, cele 6 acțiuni principale, apoi activitate recentă, progres și
Premium, iar dedesubt statistici și obiectivul de azi."""

import datetime
import html

import pandas as pd
import streamlit as st

from abonamente import deschide_abonamente
from baza_date import _client, obiectiv_zilnic, utilizator_curent
from comutator_mod import mod_ui
from limbi import limba_ui, nume_tab, t
from utile_pagini import imagine_uri, mergi

BUC = "Europe/Bucharest"

# iconițe simple, desenate aici (nu depind de nicio bibliotecă)
IC = {
    "quiz": '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.6 2.2c-.8.4-1.2 1-1.2 1.8"/><path d="M12 17h.01"/>',
    "clip": '<rect x="6" y="4.5" width="12" height="16" rx="2"/><path d="M9 4.5V3h6v1.5M9 10h6M9 14h6"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9l-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z" fill="#FFFFFF"/>',
    "stea": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.9l-5.2 2.8 1-5.9-4.3-4.1 5.9-.8z"/>',
    "cards": '<rect x="4" y="7" width="13" height="11" rx="2"/><path d="M8 4h11a1 1 0 0 1 1 1v9M8 11h5"/>',
    "doc": '<path d="M7 3.5h7l4 4V20.5H7z"/><path d="M14 3.5V8h4M9.5 12h5M9.5 15.5h5"/>',
    "chat": '<path d="M5 5h14a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-7l-4 3.5V16H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1z"/><path d="M10.3 9.3a1.8 1.8 0 1 1 2.6 1.6c-.6.3-.9.7-.9 1.3M12 13.8h.01"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "bolt": '<path d="M13 3L6 13.5h5L10 21l8-11h-5z"/>',
    "bars": '<path d="M5 20V11M12 20V5M19 20v-6"/>',
    "cal": '<rect x="4" y="5.5" width="16" height="14.5" rx="2"/><path d="M4 10h16M8 3.5v3M16 3.5v3"/>',
    "crown": '<path d="M3.5 18.5L5 8l4.5 4L12 6l2.5 6L19 8l1.5 10.5z" fill="#F5B83D" stroke="#F5B83D"/>',
    "trofeu": '<path d="M8 4h8v5a4 4 0 0 1-8 0z" fill="#F5B83D" stroke="#F5B83D"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4" stroke="#F5B83D"/><path d="M12 13v4M8.5 19h7" stroke="#F5B83D"/>',
    "upload": '<path d="M7 18a4.5 4.5 0 0 1-.6-8.96A6 6 0 0 1 18 8.5a4 4 0 0 1-.5 7.97"/><path d="M12 12v8M9 15l3-3 3 3"/>',
}


def _svg(cheie, tam=22, culoare="#FFFFFF", latime=1.8):
    return (
        f'<svg viewBox="0 0 24 24" width="{tam}" height="{tam}" fill="none" '
        f'stroke="{culoare}" stroke-width="{latime}" stroke-linecap="round" '
        f'stroke-linejoin="round">{IC[cheie]}</svg>'
    )


def _t2(ro, en):
    """Text scurt în limba interfeței (pentru textele noi, fără fișierul de traduceri)."""
    return ro if limba_ui() == "ro" else en


# (nume secțiune, cod, iconiță, culoare sus, culoare jos)
CARDURI = (
    ("Quiz", "quiz", "quiz", "#FF5C7C", "#E8336D"),
    ("Examen", "examen", "clip", "#FF9A4D", "#F2681C"),
    ("SAT", "sat", "star", "#5B9BFF", "#2F6BEA"),
    ("Flashcarduri", "carduri", "cards", "#A77BFF", "#7A45F0"),
    ("Rezumat", "rezumat", "doc", "#3FD58A", "#1FA35C"),
    ("Întreabă", "intreaba", "chat", "#BE7BFF", "#8E4BEE"),
)


# ------------------------- date -------------------------
def _randuri():
    """Ultimele rezultate salvate (cele mai noi primele). Fără cont: listă goală."""
    user = utilizator_curent()
    if user is None:
        return []
    try:
        rezultat = (
            _client()
            .table("progres")
            .select("sectiune, scor, total, creat_la")
            .eq("user_id", user.id)
            .order("creat_la", desc=True)
            .limit(1000)
            .execute()
        )
        return rezultat.data or []
    except Exception:
        return []


def _ts(valoare):
    try:
        return pd.to_datetime(valoare, utc=True)
    except Exception:
        return None


def _zi(valoare):
    try:
        return pd.to_datetime(valoare, utc=True).tz_convert(BUC).date()
    except Exception:
        return None


def _medie(randuri):
    procente = [100 * r["scor"] / r["total"] for r in randuri if r.get("total")]
    return sum(procente) / len(procente) if procente else None


def _num(valoare, zecimale=1):
    text = f"{valoare:.{zecimale}f}"
    return text.replace(".", ",") if limba_ui() == "ro" else text


def _perioade(toate):
    """Rezultatele din ultimele 7 zile și din cele 7 dinainte."""
    acum = pd.Timestamp.now(tz="UTC")
    curente, precedente = [], []
    for r in toate:
        moment = _ts(r.get("creat_la"))
        if moment is None:
            continue
        zile = (acum - moment).total_seconds() / 86400
        if zile <= 7:
            curente.append(r)
        elif zile <= 14:
            precedente.append(r)
    return curente, precedente


def _trend(valoare, text):
    """Săgeată colorată (verde în sus, roșie în jos). Fără valoare: nimic."""
    if valoare is None:
        return ""
    if valoare > 0:
        clasa, sageata = "sus", "↑"
    elif valoare < 0:
        clasa, sageata = "jos", "↓"
    else:
        clasa, sageata = "egal", "→"
    return f'<span class="aca-tr {clasa}">{sageata} {html.escape(text)}</span>'


def _serie(toate):
    """Câte zile la rând (până azi sau ieri) are cel puțin un rezultat."""
    zile = {d for d in (_zi(r.get("creat_la")) for r in toate) if d}
    ziua = pd.Timestamp.now(tz=BUC).date()
    if ziua not in zile:
        ziua = ziua - datetime.timedelta(days=1)
    n = 0
    while ziua in zile:
        n += 1
        ziua = ziua - datetime.timedelta(days=1)
    return n


def _timp(valoare):
    moment = _ts(valoare)
    if moment is None:
        return ""
    secunde = (pd.Timestamp.now(tz="UTC") - moment).total_seconds()
    if secunde < 60:
        return t("ac.acum")
    if secunde < 3600:
        return t("ac.acum_min", n=int(secunde // 60))
    if secunde < 86400:
        return t("ac.acum_h", n=int(secunde // 3600))
    zile = int(secunde // 86400)
    if zile == 1:
        return t("ac.acum_zi")
    if zile < 7:
        return t("ac.acum_zile", n=zile)
    return moment.tz_convert(BUC).strftime("%d.%m.%Y")


def _nume_tip(cod):
    cheie = f"pr.tip.{cod}"
    nume = t(cheie)
    return cod if nume == cheie else nume


def _titlu_card(icoana, text):
    return (
        '<div class="aca-ch">'
        f'<span class="aca-chi">{_svg(icoana, 20, "#A78BFA", 2)}</span>'
        f'<span class="aca-card-titlu">{html.escape(text)}</span></div>'
    )


# ------------------------- piese -------------------------
def _hero():
    """Bun venit pe două rânduri, cu robotul în dreapta."""
    user = utilizator_curent()
    robot = (
        imagine_uri("robot_hero_luminos.png")
        if mod_ui() == "light"
        else imagine_uri("robot_hero.png", "mascota.png")
    )
    img = f'<img class="aca-robot" src="{robot}" alt="">' if robot else ""
    if user is not None and getattr(user, "email", None):
        nume = user.email.split("@")[0]
        nume = nume[:1].upper() + nume[1:]
        salut = html.escape(t("ac.salut_inceput")).rstrip()
        titlu = f'{salut}<br><span class="aca-nume">{html.escape(nume)}</span>!'
    else:
        titlu = html.escape(t("ac.salut_viz"))
    sub = html.escape(t("ac.sub"))

    with st.container(key="aca_hero"):
        st.markdown(
            '<div class="aca-hero-text">'
            f'<div class="aca-titlu">{titlu}</div>'
            f'<div class="aca-sub">{sub}</div>'
            f"</div>{img}",
            unsafe_allow_html=True,
        )


def _zona_incarcare(mat):
    """Caseta mare cu margine punctată: alegerea materialului (duce la Documente)."""
    if mat is not None:
        nume_mat = t("material.text_lipit") if mat["nume"] == "Text lipit" else mat["nume"]
        titlu = html.escape(nume_mat).replace("$", "&#36;")
        sub = html.escape(
            _t2(
                "Material ales. Poți începe un quiz, un examen sau flashcarduri.",
                "Material selected. You can start a quiz, an exam or flashcards.",
            )
        )
        eticheta = t("ac.schimba")
    else:
        titlu = html.escape(_t2("Încarcă materialele tale", "Upload your materials"))
        sub = html.escape(
            _t2(
                "PDF, Word, text sau notițe lipite: orice material de studiu",
                "PDF, Word, text or pasted notes: any study material",
            )
        )
        eticheta = t("ac.alege_material")

    with st.container(key="aca_upload"):
        st.markdown(
            '<div class="aca-up">'
            f'<span class="aca-up-ic">{_svg("upload", 34, "#8B5CF6", 1.7)}</span>'
            f'<div class="aca-up-t">{titlu}</div>'
            f'<div class="aca-up-s">{sub}</div></div>',
            unsafe_allow_html=True,
        )
        _stanga, mijloc, _dreapta = st.columns([1.3, 1, 1.3])
        mijloc.button(
            eticheta,
            key="aca_alege_fisiere",
            icon=":material/upload:",
            on_click=mergi,
            args=("documente",),
            type="primary",
            use_container_width=True,
        )


def _carduri():
    """Cele 6 acțiuni principale, pe un singur rând."""
    with st.container(key="aca_cards"):
        coloane = st.columns(6, gap="small")
        for col, (nume_s, cod, ic, c1, c2) in zip(coloane, CARDURI):
            titlu_c = html.escape(nume_tab(nume_s))
            desc = html.escape(t(f"ac.c.{cod}.d"))
            with col:
                with st.container(key=f"aca_card_{cod}"):
                    st.markdown(
                        '<div class="aca-c">'
                        f'<span class="aca-ci" style="background:linear-gradient(145deg,{c1},{c2})">'
                        f"{_svg(ic, 22)}</span>"
                        f'<div class="aca-ct">{titlu_c}</div>'
                        f'<div class="aca-cd">{desc}</div></div>',
                        unsafe_allow_html=True,
                    )
                    # butonul acoperă tot cardul (invizibil, vezi stil_tema.py)
                    st.button(
                        nume_tab(nume_s),
                        key=f"aca_cb_{cod}",
                        on_click=mergi,
                        args=(nume_s,),
                    )


def _progres(toate, mat):
    user = utilizator_curent()
    medie = _medie(toate)
    medie_int = round(medie) if medie is not None else 0

    if user is None:
        mesaj = t("ac.vizitator_progres")
    elif not toate:
        mesaj = t("ac.fara_date")
    elif medie_int >= 70:
        mesaj = t("ac.mesaj_bun")
    else:
        mesaj = t("ac.mesaj_incurajare")

    serie = _serie(toate)
    text_serie = t("ac.zi_unu") if serie == 1 else t("ac.zile", n=serie)

    def rand(icoana, continut):
        return (
            f'<div class="aca-pg-r"><span class="aca-pg-ic">{icoana}</span>'
            f"<div>{continut}</div></div>"
        )

    lista = (
        rand(
            _svg("stea", 18, "#8B5CF6", 2),
            f'<div class="aca-pg-m">{html.escape(mesaj)}</div>',
        )
        + rand(
            _svg("check", 18, "#8B5CF6", 2.2),
            f'<div class="aca-pg-v">{len(toate)}</div>'
            f'<div class="aca-pg-l">{html.escape(t("ac.stat.activitati"))}</div>',
        )
        + rand(
            _svg("bolt", 18, "#8B5CF6", 2),
            f'<div class="aca-pg-v">{html.escape(text_serie)}</div>'
            f'<div class="aca-pg-l">{html.escape(t("ac.stat.serie"))}</div>',
        )
    )

    with st.container(key="aca_progres"):
        st.markdown(
            _titlu_card("trend", t("ac.progres"))
            + '<div class="aca-pg">'
            f'<div class="aca-inel" style="--p:{medie_int}"><div class="aca-inel-in">'
            f"<b>{medie_int}%</b><span>{html.escape(t('ac.rata'))}</span>"
            "</div></div>"
            f'<div class="aca-pg-lista">{lista}</div></div>',
            unsafe_allow_html=True,
        )
        st.button(
            t("ac.continua"),
            key="aca_continua",
            icon=":material/star:",
            on_click=mergi,
            args=("Quiz" if mat is not None else "documente",),
            use_container_width=True,
        )


def _rand_recent(r):
    cod = r["sectiune"]
    if cod == "preda":
        sub = t("ac.puncte", s=r["scor"], n=r["total"])
    else:
        sub = t("ac.corecte", s=r["scor"], n=r["total"])
    if cod == "quiz":
        clasa, ic = "ri-q", "quiz"
    elif cod == "examen":
        clasa, ic = "ri-e", "check"
    else:
        clasa, ic = "ri-d", "doc"
    nume = html.escape(_nume_tip(cod))
    cand = html.escape(_timp(r.get("creat_la", "")))
    return (
        f'<li><span class="aca-ri {clasa}">{_svg(ic, 18)}</span>'
        f'<div class="aca-rt"><b>{nume}</b><small>{html.escape(sub)}</small></div>'
        f"<em>{cand}</em></li>"
    )


def _recent(toate):
    with st.container(key="aca_recent"):
        c1, c2 = st.columns([2, 1], vertical_alignment="center")
        c1.markdown(_titlu_card("clock", t("ac.recent")), unsafe_allow_html=True)
        c2.button(
            f"{t('ac.vezi_toate')} →",
            key="aca_vezi_tot",
            on_click=mergi,
            args=("Progresul meu",),
            use_container_width=True,
        )
        ultimele = toate[:3]
        if not ultimele:
            st.markdown(
                f'<div class="aca-mesaj">{html.escape(t("ac.recent_gol"))}</div>',
                unsafe_allow_html=True,
            )
            return
        lista = "".join(_rand_recent(r) for r in ultimele)
        st.markdown(f'<ul class="aca-rec">{lista}</ul>', unsafe_allow_html=True)


def _premium():
    """Bannerul de Premium, cu avantajele reale din planul Premium."""
    robot = imagine_uri("robot_premium.png")
    img = f'<img class="aca-prem-robot" src="{robot}" alt="">' if robot else ""
    avantaje = "".join(
        f"<li>{html.escape(t(f'abon_av_premium_{n}'))}</li>" for n in (2, 3, 4, 6)
    )
    with st.container(key="aca_premium"):
        st.markdown(
            '<div class="aca-pb">'
            f'<div class="aca-pb-t"><span class="aca-coroana">{_svg("crown", 26, "#F5B83D", 1.6)}</span>'
            f'{html.escape(t("ac.prem.banner"))}</div>'
            f'<div class="aca-pb-s">{html.escape(t("ac.prem.banner_sub"))}</div>'
            f'<ul class="aca-pb-l">{avantaje}</ul></div>{img}',
            unsafe_allow_html=True,
        )
        col_buton, _liber = st.columns([1.6, 1.4])
        if col_buton.button(
            f"{t('ac.prem.titlu')} →",
            key="aca_prem_btn",
            type="primary",
            use_container_width=True,
        ):
            deschide_abonamente()
        st.markdown(
            f'<div class="aca-mesaj">{html.escape(t("abon_prototip_text"))}</div>',
            unsafe_allow_html=True,
        )


def _tile(culoare, icoana, eticheta, valoare, trend=""):
    return (
        '<div class="aca-tile">'
        f'<span class="aca-ti" style="background:{culoare}">{icoana}</span>'
        f'<div><div class="aca-tl">{html.escape(eticheta)}</div>'
        f'<div class="aca-tv">{valoare}{trend}</div></div></div>'
    )


def _stats(toate):
    curente, precedente = _perioade(toate)

    var_nr = None
    if precedente:
        var_nr = round(100 * (len(curente) - len(precedente)) / len(precedente))
    trend_nr = _trend(var_nr, f"{abs(var_nr)}%") if var_nr is not None else ""

    medie = _medie(toate)
    m_cur, m_prec = _medie(curente), _medie(precedente)
    trend_medie = ""
    if m_cur is not None and m_prec is not None:
        dif = round(m_cur - m_prec, 1)
        trend_medie = _trend(dif, _num(abs(dif)) + "%")

    serie = _serie(toate)
    text_serie = t("ac.zi_unu") if serie == 1 else t("ac.zile", n=serie)
    text_medie = f"{_num(medie)}%" if medie is not None else "—"

    tiles = (
        _tile(
            "rgba(31,163,92,0.25)",
            _svg("check", 22, "#3FD58A", 2.4),
            t("ac.stat.activitati"),
            str(len(toate)),
            trend_nr,
        )
        + _tile(
            "rgba(245,184,61,0.18)",
            _svg("trofeu", 22),
            t("ac.stat.media"),
            html.escape(text_medie),
            trend_medie,
        )
        + _tile(
            "rgba(139,92,246,0.25)",
            _svg("bolt", 22, "#B58BFF", 2),
            t("ac.stat.serie"),
            html.escape(text_serie),
        )
    )
    with st.container(key="aca_stats"):
        st.markdown(
            _titlu_card("bars", t("ac.stat.titlu"))
            + f'<div class="aca-grila">{tiles}</div>',
            unsafe_allow_html=True,
        )


def _obiectiv(toate, mat):
    try:
        tinta = int(obiectiv_zilnic())
    except Exception:
        tinta = 2
    azi = pd.Timestamp.now(tz=BUC).date()
    facute = sum(1 for r in toate if _zi(r.get("creat_la")) == azi)
    procent = min(100, round(100 * facute / tinta)) if tinta else 0
    if facute >= tinta:
        mesaj = t("ob.atins")
    else:
        ramase = tinta - facute
        cuvant = t("ob.activitate") if ramase == 1 else t("ob.activitati")
        mesaj = t("ob.ramase", r=ramase, cuvant=cuvant)

    with st.container(key="aca_obiectiv"):
        st.markdown(
            _titlu_card("cal", t("ac.obiectiv.titlu"))
            + '<div class="aca-ob">'
            f'<span class="aca-ob-ic">{_svg("cal", 34, "#B58BFF", 1.6)}</span>'
            f'<div><div class="aca-ob-t">{html.escape(t("ac.obiectiv.progres", c=facute, n=tinta))}</div>'
            f'<div class="aca-bara"><i style="width:{procent}%"></i></div>'
            f'<div class="aca-mesaj">{html.escape(mesaj)}</div></div></div>',
            unsafe_allow_html=True,
        )
        st.button(
            f"{t('ac.incepe_acum')} →",
            key="aca_incepe_acum",
            on_click=mergi,
            args=("Quiz" if mat is not None else "documente",),
            type="primary",
            use_container_width=True,
        )


def afiseaza_acasa(mat=None):
    """mat = materialul ales (sau None dacă nu e ales niciunul)."""
    # marcaj: CSS-ul lărgește pagina doar când acest element există
    st.markdown('<div class="aca-marker"></div>', unsafe_allow_html=True)
    toate = _randuri()

    _hero()
    _zona_incarcare(mat)
    _carduri()

    r1, r2, r3 = st.columns([1.15, 1.1, 1.3], gap="medium")
    with r1:
        _recent(toate)
    with r2:
        _progres(toate, mat)
    with r3:
        _premium()

    r4, r5 = st.columns([2.3, 1], gap="large")
    with r4:
        _stats(toate)
    with r5:
        _obiectiv(toate, mat)
