"""Secțiune: Plan de studiu până la examen.

Alegi data examenului și câte minute ai pe zi, iar aplicația împarte partea
aleasă din material pe zilele rămase, cu zile de recapitulare la final.
Nu face nicio cerere la Google și nu salvează nimic pe cont; planul se poate
descărca pentru printat.
"""

import datetime
import html
import math

import streamlit as st

from limbi import descriere_sectiune, limba_ui, t, unitate_sg, unitate_ui
from stil_sectiuni import injecteaza_stiluri

NUME = "Plan de studiu"
ORDINE = 70
CERE_MATERIAL = True
DESCRIERE = (
    "Alegi data examenului și câte minute ai pe zi, iar aplicația împarte "
    "materialul pe zile, cu zile de recapitulare la final. Planul se poate "
    "descărca pentru printat."
)

VITEZA_STUDIU = 800  # caractere pe minut: o estimare, nu o măsurătoare
MAX_ZILE_PANA_LA_EXAMEN = 120
MAX_ZILE_RECAPITULARE = 2

ZILE_SAPT = {
    "ro": ["lun", "mar", "mie", "joi", "vin", "sâm", "dum"],
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
}
LUNI = {
    "ro": ["ian", "feb", "mar", "apr", "mai", "iun", "iul", "aug", "sep", "oct", "nov", "dec"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

CSS_HTML = (
    "body{font-family:Arial,Helvetica,sans-serif;max-width:760px;margin:2rem auto;"
    "padding:0 1rem;color:#111;line-height:1.5}"
    "h1{margin-bottom:0.2rem}.sub{color:#555;margin-bottom:1.5rem}"
    ".zi{border:1px solid #ccc;border-left:4px solid #E5383B;border-radius:6px;"
    "padding:0.6rem 1rem;margin:0.7rem 0;page-break-inside:avoid}"
    ".zi h3{margin:0 0 0.3rem;font-size:1.05rem}.zi p{margin:0.15rem 0}"
    ".act{color:#444}"
)


def _azi():
    """Data de azi, în ora României."""
    try:
        from zoneinfo import ZoneInfo

        return datetime.datetime.now(ZoneInfo("Europe/Bucharest")).date()
    except Exception:
        return datetime.date.today()


def _data_text(d):
    lb = "ro" if limba_ui() == "ro" else "en"
    return f"{ZILE_SAPT[lb][d.weekday()]}, {d.day} {LUNI[lb][d.month - 1]}"


def _minute(caractere):
    """Minute estimate, rotunjite în sus la multipli de 5."""
    m = math.ceil(caractere / VITEZA_STUDIU)
    return max(5, 5 * math.ceil(m / 5))


def _imparte(unitati, zile):
    """Împarte unitățile (în ordine) în `zile` grupuri, cam egale ca număr de
    caractere. Fiecare grup are cel puțin o unitate."""
    n = len(unitati)
    zile = max(1, min(zile, n))
    marimi = [max(1, len(u["text"])) for u in unitati]
    ramas_total = sum(marimi)
    grupuri = []
    i = 0
    for z in range(zile):
        zile_ramase = zile - z
        if zile_ramase == 1:
            grupuri.append(unitati[i:])
            break
        tinta = ramas_total / zile_ramase
        curent, s = [], 0
        while i < n - (zile_ramase - 1):
            if curent and s + marimi[i] / 2 > tinta:
                break
            curent.append(unitati[i])
            s += marimi[i]
            ramas_total -= marimi[i]
            i += 1
        grupuri.append(curent)
    return grupuri


def _construieste(unitati, azi, examen):
    """Întoarce (zilele planului, data de start). Ziua examenului nu intră în plan."""
    d = (examen - azi).days
    n = len(unitati)
    recap = 0 if d < 3 else (1 if d <= 7 else MAX_ZILE_RECAPITULARE)
    zile_studiu = max(1, min(d - recap, n))
    grupuri = _imparte(unitati, zile_studiu)
    zile_plan = len(grupuri) + recap
    start = examen - datetime.timedelta(days=zile_plan)

    zile = []
    for k, g in enumerate(grupuri):
        zile.append(
            {
                "tip": "studiu",
                "data": start + datetime.timedelta(days=k),
                "unitati": g,
                "caractere": sum(len(u["text"]) for u in g),
            }
        )
    for k in range(recap):
        zile.append(
            {
                "tip": "recapitulare",
                "data": start + datetime.timedelta(days=len(grupuri) + k),
            }
        )
    return zile, start


def _interval(eticheta, grup):
    a, b = grup[0]["pagina"], grup[-1]["pagina"]
    if a == b:
        return f"{unitate_sg(eticheta, majuscula=True)} {a}"
    return f"{unitate_ui(eticheta).capitalize()} {a}-{b}"


def _linii(zile, examen, eticheta):
    """Planul ca listă de (titlu, detaliu, activitate)."""
    linii = []
    nr = 0
    for z in zile:
        data = _data_text(z["data"])
        if z["tip"] == "studiu":
            nr += 1
            detaliu = (
                f"{_interval(eticheta, z['unitati'])} · "
                f"{t('pl.minute', m=_minute(z['caractere']))}"
            )
            linii.append(
                (t("pl.ziua", n=nr, data=data), detaliu, t("pl.act_studiu"))
            )
        else:
            linii.append(
                (
                    t("pl.recap_titlu", data=data),
                    t("pl.recap_detaliu"),
                    t("pl.act_recap"),
                )
            )
    linii.append(
        (
            t("pl.examen_titlu", data=_data_text(examen)),
            t("pl.examen_detaliu"),
            "",
        )
    )
    return linii


def _markdown(linii):
    bucati = []
    for titlu, detaliu, activitate in linii:
        parti = [f"**{titlu}**", detaliu, activitate]
        bucati.append("  \n".join(p for p in parti if p))
    return "\n\n".join(bucati)


def _html(linii, titlu_doc, subtitlu):
    limba = "ro" if limba_ui() == "ro" else "en"
    zile = ""
    for titlu, detaliu, activitate in linii:
        zile += (
            '<div class="zi">'
            f"<h3>{html.escape(titlu)}</h3>"
            f"<p>{html.escape(detaliu)}</p>"
        )
        if activitate:
            zile += f'<p class="act">{html.escape(activitate)}</p>'
        zile += "</div>"
    return (
        f'<!DOCTYPE html><html lang="{limba}"><head><meta charset="utf-8">'
        f"<title>{html.escape(titlu_doc)}</title>"
        "<style>" + CSS_HTML + "</style></head><body>"
        f"<h1>{html.escape(titlu_doc)}</h1>"
        f'<div class="sub">{html.escape(subtitlu)}</div>'
        + zile
        + "</body></html>"
    )


def afiseaza(ctx):
    """Funcția pe care o apelează aplicația pentru această secțiune."""
    injecteaza_stiluri()
    st.caption(descriere_sectiune(NUME, DESCRIERE))

    azi = _azi()
    with st.container(border=True):
        c1, c2 = st.columns(2)
        examen = c1.date_input(
            t("pl.data"),
            value=azi + datetime.timedelta(days=14),
            min_value=azi + datetime.timedelta(days=1),
            max_value=azi + datetime.timedelta(days=MAX_ZILE_PANA_LA_EXAMEN),
            format="DD/MM/YYYY",
            key="pl_data",
        )
        minute_zi = c2.number_input(
            t("pl.minute_zi"), 15, 480, 60, step=15, key="pl_min"
        )

    if not isinstance(examen, datetime.date):
        return

    unitati = ctx.selectate
    zile, start = _construieste(unitati, azi, examen)
    zile_pana = (examen - azi).days
    n_studiu = sum(1 for z in zile if z["tip"] == "studiu")
    n_recap = len(zile) - n_studiu
    max_min = max(_minute(z["caractere"]) for z in zile if z["tip"] == "studiu")

    m1, m2, m3 = st.columns(3)
    m1.metric(t("pl.m_pana"), zile_pana)
    m2.metric(t("pl.m_studiu"), n_studiu)
    m3.metric(t("pl.m_recap"), n_recap)

    if max_min > minute_zi:
        st.warning(t("pl.prea_incarcat", max=max_min, minute=int(minute_zi)))
    else:
        st.success(t("pl.ok", max=max_min))
    if start > azi:
        st.info(t("pl.incepe_pe", data=_data_text(start)))
    st.caption(t("pl.estimare", v=VITEZA_STUDIU))

    linii = _linii(zile, examen, ctx.eticheta)
    st.markdown(_markdown(linii))

    nume = ctx.mat["nume"]
    if nume == "Text lipit":
        nume = t("material.text_lipit")
    st.download_button(
        t("pl.descarca"),
        data=_html(
            linii,
            t("pl.titlu_doc"),
            t("pl.subtitlu_doc", nume=nume, data=_data_text(examen)),
        ),
        file_name="plan_de_studiu.html",
        mime="text/html",
        on_click="ignore",
        key="pl_dl",
    )
