"""Pagina Acasă: bun venit, progres, acțiuni rapide, activitate recentă."""

import html

import pandas as pd
import streamlit as st

from abonamente import deschide_abonamente
from baza_date import _client, utilizator_curent
from limbi import nume_tab, t
from navigare import ICONITE
from utile_pagini import logo_uri, mergi


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


def _in_perioada(rand, limita):
    try:
        return pd.to_datetime(rand["creat_la"], utc=True) >= limita
    except Exception:
        return True


def _statistici(randuri):
    procente = [100 * r["scor"] / r["total"] for r in randuri if r.get("total")]
    medie = round(sum(procente) / len(procente)) if procente else 0
    quiz = sum(1 for r in randuri if r["sectiune"] == "quiz")
    examene = sum(1 for r in randuri if r["sectiune"] == "examen")
    return medie, quiz, examene, len(randuri) - quiz - examene


def _timp(valoare):
    try:
        moment = pd.to_datetime(valoare, utc=True)
        secunde = (pd.Timestamp.now(tz="UTC") - moment).total_seconds()
    except Exception:
        return ""
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
    return moment.tz_convert("Europe/Bucharest").strftime("%d.%m.%Y")


def _nume_tip(cod):
    cheie = f"pr.tip.{cod}"
    nume = t(cheie)
    return cod if nume == cheie else nume


# ------------------------- piese -------------------------
def _hero():
    user = utilizator_curent()
    uri = logo_uri()
    logo = f'<img class="aca-logo" src="{uri}" alt="">' if uri else ""
    if user is not None and getattr(user, "email", None):
        nume = user.email.split("@")[0]
        nume = nume[:1].upper() + nume[1:]
        titlu = (
            f'{html.escape(t("ac.salut_inceput"))}'
            f'<span class="aca-nume">{html.escape(nume)}</span>!'
        )
    else:
        titlu = html.escape(t("ac.salut_viz"))

    with st.container(key="aca_hero"):
        st.markdown(
            '<div class="aca-hero-text">'
            f'<div class="aca-titlu">{titlu}</div>'
            f'<div class="aca-sub">{html.escape(t("ac.sub"))}</div>'
            f"</div>{logo}",
            unsafe_allow_html=True,
        )
        coloane = st.columns([1, 1, 1, 1.6])
        for col, (nume_s, cod) in zip(
            coloane, (("Quiz", "quiz"), ("Examen", "examen"), ("SAT", "sat"))
        ):
            col.button(
                nume_tab(nume_s),
                key=f"aca_h_{cod}",
                icon=f":material/{ICONITE.get(nume_s, 'apps')}:",
                on_click=mergi,
                args=(nume_s,),
                use_container_width=True,
            )


def _progres(toate):
    user = utilizator_curent()
    with st.container(key="aca_progres"):
        h1, h2 = st.columns([1.3, 1])
        h1.markdown(
            f'<div class="aca-card-titlu">{html.escape(t("ac.progres"))}</div>',
            unsafe_allow_html=True,
        )
        perioada = h2.selectbox(
            t("ac.perioada"),
            ["7", "tot"],
            format_func=lambda v: t(f"ac.perioada_{v}"),
            key="aca_perioada",
            label_visibility="collapsed",
        )
        randuri = toate
        if perioada == "7":
            limita = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
            randuri = [r for r in toate if _in_perioada(r, limita)]
        medie, quiz, examene, alte = _statistici(randuri)

        if user is None:
            mesaj = t("ac.vizitator_progres")
        elif not randuri:
            mesaj = t("ac.fara_date")
        elif medie >= 70:
            mesaj = t("ac.mesaj_bun")
        else:
            mesaj = t("ac.mesaj_incurajare")

        randuri_html = (
            (t("ac.quizuri"), quiz, "p1"),
            (t("ac.examene"), examene, "p2"),
            (t("ac.alte"), alte, "p3"),
        )
        lista = "".join(
            f'<li><i class="aca-pct {c}"></i><span>{html.escape(n)}</span>'
            f"<b>{v}</b></li>"
            for n, v, c in randuri_html
        )
        st.markdown(
            '<div class="aca-prog">'
            f'<div class="aca-inel" style="--p:{medie}"><div class="aca-inel-in">'
            f'<b>{medie}%</b><span>{html.escape(t("ac.scor_mediu"))}</span>'
            "</div></div>"
            f'<ul class="aca-rows">{lista}</ul></div>'
            f'<div class="aca-mesaj">{html.escape(mesaj)}</div>',
            unsafe_allow_html=True,
        )


def _rapide():
    actiuni = (
        ("quiz", "Quiz"),
        ("examen", "Examen"),
        ("rezumat", "Rezumat"),
        ("intreaba", "Întreabă"),
    )
    with st.container(key="aca_rapide"):
        st.markdown(
            f'<div class="aca-card-titlu">{html.escape(t("ac.rapide"))}</div>',
            unsafe_allow_html=True,
        )
        r1 = st.columns(2)
        r2 = st.columns(2)
        for celula, (cod, pagina) in zip(r1 + r2, actiuni):
            with celula:
                with st.container(key=f"aca_q_{cod}"):
                    st.markdown(
                        f'<div class="aca-q-t">{html.escape(t(f"ac.q.{cod}.t"))}</div>'
                        f'<div class="aca-q-d">{html.escape(t(f"ac.q.{cod}.d"))}</div>',
                        unsafe_allow_html=True,
                    )
                    st.button(
                        t("ac.start"),
                        key=f"aca_qb_{cod}",
                        icon=f":material/{ICONITE.get(pagina, 'apps')}:",
                        on_click=mergi,
                        args=(pagina,),
                        use_container_width=True,
                    )


def _recent(toate):
    with st.container(key="aca_recent"):
        c1, c2 = st.columns([2, 1])
        c1.markdown(
            f'<div class="aca-card-titlu">{html.escape(t("ac.recent"))}</div>',
            unsafe_allow_html=True,
        )
        c2.button(
            t("ac.vezi_tot"),
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
        lista = "".join(
            '<li><i class="aca-dot"></i>'
            f'<span>{html.escape(_nume_tip(r["sectiune"]))} · '
            f'{r["scor"]}/{r["total"]}</span>'
            f'<em>{html.escape(_timp(r.get("creat_la", "")))}</em></li>'
            for r in ultimele
        )
        st.markdown(f'<ul class="aca-rec">{lista}</ul>', unsafe_allow_html=True)


def _premium():
    with st.container(key="aca_premium"):
        st.markdown(
            f'<div class="aca-prem-t">{html.escape(t("ac.prem.titlu"))}</div>'
            f'<div class="aca-prem-d">{html.escape(t("ac.prem.text"))}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            t("ac.prem.btn"),
            key="aca_prem_btn",
            icon=":material/workspace_premium:",
        ):
            deschide_abonamente()


def afiseaza_acasa():
    # marcaj: CSS-ul lărgește pagina doar când acest element există
    st.markdown('<div class="aca-marker"></div>', unsafe_allow_html=True)
    toate = _randuri()
    _hero()
    c1, c2 = st.columns([1, 1.15])
    with c1:
        _progres(toate)
    with c2:
        _rapide()
    c3, c4 = st.columns([1.15, 1])
    with c3:
        _recent(toate)
    with c4:
        _premium()
