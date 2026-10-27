"""Secțiune: Găsește greșeala.

Un paragraf scurt din material, în care o propoziție a fost modificată subtil.
Alegi propoziția pe care o crezi modificată și vezi ce spunea de fapt textul.
La final primești scorul și ce să recapitulezi.
"""

import streamlit as st

from baza_date import salveaza_progres
from generare_greseala import genereaza_teanc_greseala
from limbi import descriere_sectiune, t, unitate_sg
from memorie import preia_din_teanc
from stil_sectiuni import injecteaza_stiluri

NUME = "Găsește greșeala"
ORDINE = 27
CERE_MATERIAL = True
DESCRIERE = (
    "Paragrafe din materialul tău, în care o propoziție a fost modificată "
    "subtil. O găsești și vezi ce spune de fapt documentul."
)

CHEIE = "gr_sesiune"


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _porneste(intrebari, info, hash_material):
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "intrebari": intrebari,
        "info": info,
        "idx": 0,
        "raspunsuri": {},  # poziția paragrafului -> poziția propoziției alese
        "progres_salvat": False,
    }


def _alege(poz):
    s = st.session_state.get(CHEIE)
    if s and s["idx"] not in s["raspunsuri"]:
        s["raspunsuri"][s["idx"]] = poz


def _urmatoarea():
    s = st.session_state.get(CHEIE)
    if s:
        s["idx"] += 1


def _inceput_nou():
    st.session_state.pop(CHEIE, None)


def _repeta_gresite():
    s = st.session_state.get(CHEIE)
    if not s:
        return
    gresite = [
        q for i, q in enumerate(s["intrebari"]) if s["raspunsuri"].get(i) != q["corect"]
    ]
    if gresite:
        _porneste(gresite, s["info"], s["hash"])


def _lista_propozitii(q):
    """Paragraful, cu propoziția modificată îngroșată."""
    linii = []
    for j, prop in enumerate(q["propozitii"]):
        text = f"({j + 1}) {_md(prop)}"
        linii.append(f"**{text}**" if j == q["corect"] else text)
    return "\n\n".join(linii)


def _setari(ctx):
    with st.container(border=True):
        c1, c2 = st.columns(2)
        nr = c1.number_input(t("gr.nr"), 3, 15, 5, key="gr_nr")
        dif = c2.selectbox(
            t("comun.dificultate"),
            ["ușoară", "medie", "grea"],
            index=1,
            format_func=lambda v: t(f"dif.{v}"),
            key="gr_dif",
        )
        porneste = st.button(
            t("sect.start"),
            key="gr_start",
            type="primary",
            use_container_width=True,
        )

    if porneste:
        with st.spinner(t("gr.spinner")):
            try:
                elemente, model, nota = preia_din_teanc(
                    ("gr", ctx.hash_material, dif, ctx.limba),
                    nr,
                    "intrebare",
                    lambda: genereaza_teanc_greseala(
                        ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
                    ),
                )
            except Exception as e_gr:
                st.error(t("comun.eroare", e=e_gr))
                return
        if not elemente:
            st.error(t("gr.fara_elemente"))
            return
        info = f"{model} · {nota}"
        if len(elemente) < nr:
            info += t("gr.doar_n", n=len(elemente))
        _porneste(elemente, info, ctx.hash_material)
        st.rerun()


def _intrebare(s):
    total = len(s["intrebari"])
    i = s["idx"]
    q = s["intrebari"][i]
    raspuns = s["raspunsuri"].get(i)
    corecte = sum(
        1 for j, a in s["raspunsuri"].items() if a == s["intrebari"][j]["corect"]
    )

    st.progress(i / total, text=t("gr.progres", i=i + 1, total=total))
    st.caption(t("comun.model", info=s["info"]))

    if raspuns is None:
        st.markdown(f"**{t('gr.intrebare')}**")
        for j, prop in enumerate(q["propozitii"]):
            st.button(
                f"({j + 1}) {_md(prop)}",
                on_click=_alege,
                args=(j,),
                key=f"gr_p_{i}_{j}",
                use_container_width=True,
            )
    else:
        if raspuns == q["corect"]:
            st.success(t("gr.corect"))
        else:
            st.error(t("gr.gresit", n=q["corect"] + 1))
        st.markdown(_lista_propozitii(q))
        st.info(t("gr.textul_spunea", x=_md(q["propozitia_corecta"])))
        if q.get("explicatie"):
            st.markdown(_md(q["explicatie"]))
        st.caption(
            f"{unitate_sg(q.get('unitate', 'pagina'), majuscula=True)} "
            f"{q.get('pagina', '?')}"
        )
        ultima = i + 1 >= total
        st.button(
            t("sect.vezi_rezultat") if ultima else t("sect.urmatoarea"),
            on_click=_urmatoarea,
            key="gr_next",
            use_container_width=True,
            type="primary",
        )
    st.caption(t("sect.corecte_pana_acum", c=corecte, n=len(s["raspunsuri"])))


def _rezultate(s):
    total = len(s["intrebari"])
    gresite = [
        (i, q)
        for i, q in enumerate(s["intrebari"])
        if s["raspunsuri"].get(i) != q["corect"]
    ]
    scor = total - len(gresite)
    procent = round(100 * scor / total)

    if not s.get("progres_salvat"):
        salveaza_progres("greseala", scor, total)
        s["progres_salvat"] = True

    st.progress(1.0, text=t("sect.terminat"))
    c1, c2 = st.columns(2)
    c1.metric(t("sect.scor"), f"{scor}/{total}")
    c2.metric(t("sect.procent"), f"{procent}%")

    if not gresite:
        st.success(t("gr.toate_corecte"))
    else:
        st.subheader(t("sect.recapitulezi"))
        with st.expander(t("gr.vezi_gresite")):
            for i, q in gresite:
                ales = s["raspunsuri"].get(i)
                st.markdown(_lista_propozitii(q))
                if ales is not None:
                    st.caption(t("gr.alegerea_ta", a=ales + 1, b=q["corect"] + 1))
                st.markdown(t("gr.textul_spunea", x=_md(q["propozitia_corecta"])))
                if q.get("explicatie"):
                    st.caption(_md(q["explicatie"]))
                st.caption(
                    f"{unitate_sg(q.get('unitate', 'pagina'), majuscula=True)} "
                    f"{q.get('pagina', '?')}"
                )
                st.divider()

    b1, b2 = st.columns(2)
    if gresite:
        b1.button(
            t("gr.repeta"),
            on_click=_repeta_gresite,
            key="gr_repeta",
            use_container_width=True,
        )
    b2.button(
        t("sect.nou"),
        on_click=_inceput_nou,
        key="gr_nou",
        use_container_width=True,
    )


def afiseaza(ctx):
    """Funcția pe care o apelează aplicația pentru această secțiune."""
    injecteaza_stiluri()
    st.caption(descriere_sectiune(NUME, DESCRIERE))

    s = st.session_state.get(CHEIE)
    if s and s["hash"] != ctx.hash_material:
        st.session_state.pop(CHEIE, None)  # s-a schimbat materialul
        s = None

    if s is None:
        _setari(ctx)
    elif s["idx"] < len(s["intrebari"]):
        _intrebare(s)
    else:
        _rezultate(s)
