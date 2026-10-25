"""Testul cu cronometru. Același cod merge și pentru examenul din document,
și pentru testul SAT."""

import time

import streamlit as st

from baza_date import salveaza_progres
from explicatii import arata_corect_si_motiv
from export_html import html_examen
from limbi import eticheta_grup_ui, sursa_ui, t, text_intrebare_ui, varianta_ui
from stil_taburi import CSS_TABURI
from utile import formateaza_timp, md


def afiseaza_intrebare(q, i, cheie):
    with st.container(border=True):
        if q.get("pasaj"):
            text = md(q["pasaj"], q)
            st.markdown("\n".join("> " + linie for linie in text.split("\n")))
        st.radio(
            md(f"{i + 1}. {text_intrebare_ui(q)}", q),
            q["variante"],
            index=None,
            key=cheie,
            format_func=lambda v, q=q: md(varianta_ui(v, q), q),
        )


def sterge_chei_examen(nume):
    """Șterge răspunsurile selectate în testul anterior."""
    prefix = f"{nume}_r"
    for k in list(st.session_state.keys()):
        if k.startswith(prefix) and k[len(prefix):].isdigit():
            del st.session_state[k]


def incheie_examen(nume, expirat=False):
    ex = st.session_state.get(nume)
    if ex and ex["stare"] == "in_curs":
        ex["raspunsuri"] = {
            i: st.session_state.get(f"{nume}_r{i}")
            for i in range(len(ex["intrebari"]))
        }
        ex["sfarsit"] = time.time()
        ex["expirat"] = expirat
        ex["stare"] = "terminat"


def examen_nou(nume):
    sterge_chei_examen(nume)
    st.session_state.pop(nume, None)


def reface_cu_greseli(nume, ex, gresite):
    """Pornește un test nou, doar cu întrebările greșite la ultima predare.
    Timpul alocat e proporțional cu numărul de întrebări greșite."""
    sterge_chei_examen(nume)
    total_initial = len(ex["intrebari"])
    durata_noua = max(60, round(ex["durata"] * len(gresite) / total_initial))
    st.session_state[nume] = {
        "sursa": ex.get("sursa"),
        "titlu": f"Recapitulare greșeli - {ex.get('titlu', 'Rezultate')}",
        "intrebari": list(gresite),
        "cerute": len(gresite),
        "durata": durata_noua,
        "info": t("comun.recapitulare"),
        "context": ex["context"],
        "stare": "in_curs",
        "start": time.time(),
    }


@st.fragment(run_every=1)
def cronometru(nume):
    """Se reîncarcă singur în fiecare secundă; la 0 predă testul. Plutește în
    colțul din dreapta sus, ca să-l vezi oriunde ai fi în pagină."""
    ex = st.session_state.get(nume)
    if not ex or ex["stare"] != "in_curs":
        return
    ramas = ex["durata"] - (time.time() - ex["start"])
    if ramas <= 0:
        incheie_examen(nume, expirat=True)
        st.rerun()
    with st.container(key=f"cronometru_fix_{nume}"):
        st.metric(t("ex.timp_ramas"), formateaza_timp(ramas))
        if ramas <= 60:
            st.warning(t("ex.sub_minut"))


def afiseaza_rezultat(ex, nume):
    intrebari = ex["intrebari"]
    total = len(intrebari)
    scor = 0
    grupuri = {}  # etichetă (pagină sau temă) -> [total, greșite]
    detalii = []

    for i, q in enumerate(intrebari):
        ales = ex["raspunsuri"].get(i)
        ok = ales == q["variante"][q["corect"]]
        if ok:
            scor += 1
        stat = grupuri.setdefault(eticheta_grup_ui(q), [0, 0])
        stat[0] += 1
        if not ok:
            stat[1] += 1
        detalii.append((i, q, ales, ok))

    # salvăm scorul pe cont o singură dată, prima oară când se afișează rezultatul
    if not ex.get("progres_salvat"):
        salveaza_progres(nume, scor, total)
        ex["progres_salvat"] = True

    procent = round(100 * scor / total)
    folosit = ex["sfarsit"] - ex["start"]
    fara_raspuns = sum(1 for _, _, ales, _ in detalii if ales is None)
    este_sat = ex.get("sursa") == "sat"

    if ex.get("expirat"):
        st.warning(t("ex.expirat"))

    c1, c2, c3 = st.columns(3)
    c1.metric(t("ex.scor"), f"{scor}/{total}")
    c2.metric(t("ex.procent"), f"{procent}%")
    c3.metric(t("ex.timp_folosit"), formateaza_timp(folosit))
    st.progress(scor / total)
    if fara_raspuns:
        st.caption(t("ex.fara_raspuns", n=fara_raspuns))

    st.subheader(t("ex.recapitulezi"))
    de_recapitulat = sorted(
        [(eticheta, tot, g) for eticheta, (tot, g) in grupuri.items() if g > 0],
        key=lambda x: (-x[2], -x[2] / x[1]),
    )
    if not de_recapitulat:
        st.success(t("ex.toate_corecte"))
    else:
        for eticheta, tot, g in de_recapitulat:
            cuvant = (
                t("ex.intrebare_gresita") if tot == 1 else t("ex.intrebari_gresite")
            )
            st.markdown(
                t("ex.grup", eticheta=eticheta, g=g, tot=tot, cuvant=cuvant)
            )
        st.caption(t("ex.nota_sat") if este_sat else t("ex.nota_doc"))
    if este_sat:
        st.caption(t("ex.nota_sat_oficial"))

    gresite_intrebari = [q for _, q, _, ok in detalii if not ok]
    if gresite_intrebari:
        st.button(
            t("ex.recap_buton", n=len(gresite_intrebari)),
            on_click=reface_cu_greseli,
            args=(nume, ex, gresite_intrebari),
            key=f"recap_{nume}",
            type="primary",
        )

    with st.expander(t("ex.vezi_toate")):
        for i, q, ales, ok in detalii:
            stare = t("ex.corect") if ok else t("ex.gresit")
            if q.get("pasaj"):
                st.markdown(md(q["pasaj"], q))
            st.markdown(f"**{i + 1}. {md(text_intrebare_ui(q), q)}**")
            raspuns_tau = md(varianta_ui(ales, q), q) if ales else t("ex.fara_raspuns_text")
            st.markdown(f"{stare}. {t('ex.raspunsul_tau', r=raspuns_tau)}")
            if not ok:
                arata_corect_si_motiv(q, ales)
            st.caption(f"{md(q['explicatie'], q)} ({sursa_ui(q)})")
            st.divider()

    st.download_button(
        t("ex.descarca"),
        data=html_examen(
            ex.get("titlu", "Rezultate examen"),
            scor,
            total,
            procent,
            folosit,
            de_recapitulat,
            detalii,
            mathjax=este_sat,
        ),
        file_name=f"{nume}_rezultate.html",
        mime="text/html",
        on_click="ignore",
        key=f"dl_{nume}",
    )
    st.button(t("ex.nou"), on_click=examen_nou, args=(nume,), key=f"nou_{nume}")


def afiseaza_examen(nume, context, formular):
    """Gestionează cele trei stări ale unui test: setări, în curs, terminat.
    `context` identifică materialul; dacă se schimbă, testul se resetează.
    `formular()` desenează setările și, când se apasă Începe, întoarce un
    dicționar cu testul (altfel None)."""
    st.markdown(CSS_TABURI, unsafe_allow_html=True)

    ex = st.session_state.get(nume)
    if ex and ex["context"] != context:
        sterge_chei_examen(nume)
        st.session_state.pop(nume, None)
        ex = None

    if ex is None:
        nou = formular()
        if nou:
            sterge_chei_examen(nume)
            nou["context"] = context
            nou["stare"] = "in_curs"
            nou["start"] = time.time()  # pornește după generare
            st.session_state[nume] = nou
            st.rerun()

    elif ex["stare"] == "in_curs":
        if time.time() - ex["start"] >= ex["durata"]:
            incheie_examen(nume, expirat=True)
            st.rerun()

        cronometru(nume)
        st.caption(t("comun.model", info=ex["info"]))
        if len(ex["intrebari"]) < ex["cerute"]:
            st.info(t("ex.mai_putine", n=len(ex["intrebari"])))
        for i, q in enumerate(ex["intrebari"]):
            afiseaza_intrebare(q, i, f"{nume}_r{i}")
        st.button(
            t("ex.preda"),
            on_click=incheie_examen,
            args=(nume,),
            key=f"preda_{nume}",
            type="primary",
        )

    else:  # terminat
        afiseaza_rezultat(ex, nume)
