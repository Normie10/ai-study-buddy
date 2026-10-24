"""Secțiune: Adevărat / Fals.

O afirmație pe rând: răspunzi cu Adevărat sau Fals și vezi imediat dacă ai
nimerit, cu explicație și sursă. La final primești scorul și ce să recapitulezi.

Așa arată orice secțiune nouă: un fișier în folderul sectiuni/ cu cele patru
setări de mai jos și o funcție afiseaza(ctx). Aplicația o găsește singură.
"""

import html
from collections import Counter

import streamlit as st

from baza_date import salveaza_progres
from export_html import html_quiz
from generare import genereaza_teanc_af
from limbi import descriere_sectiune, eticheta_grup_ui, t, unitate_sg
from memorie import preia_din_teanc
from stil_sectiuni import injecteaza_stiluri

NUME = "Adevărat / Fals"
ORDINE = 25  # poziția în listă: numerele mici apar primele
CERE_MATERIAL = True  # False = merge și fără document (ca SAT)
DESCRIERE = (
    "Afirmații din materialul tău. Răspunzi pe rând cu Adevărat sau Fals și vezi "
    "imediat dacă ai nimerit, cu explicație și sursa din document."
)

CHEIE = "afs_sesiune"  # unde ținem în memorie sesiunea curentă


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _html(text):
    """Text sigur pentru HTML: fără etichete, fără formule, cu rânduri noi."""
    return html.escape(str(text)).replace("$", "&#36;").replace("\n", "<br>")


def _var(idx):
    """Numele variantei (0 = Adevărat, 1 = Fals), în limba interfeței."""
    return t("af.adevarat") if idx == 0 else t("af.fals")


def _porneste(intrebari, info, hash_material):
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "intrebari": intrebari,
        "info": info,
        "idx": 0,
        "raspunsuri": {},  # poziția afirmației -> 0 (Adevărat) sau 1 (Fals)
        "progres_salvat": False,
    }


def _raspunde(alegere):
    s = st.session_state.get(CHEIE)
    if s and s["idx"] not in s["raspunsuri"]:
        s["raspunsuri"][s["idx"]] = alegere


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


def _setari(ctx):
    with st.container(border=True):
        c1, c2 = st.columns(2)
        nr = c1.number_input(t("af.nr"), 3, 30, 10, key="afs_nr")
        dif = c2.selectbox(
            t("comun.dificultate"),
            ["ușoară", "medie", "grea"],
            index=1,
            format_func=lambda v: t(f"dif.{v}"),
            key="afs_dif",
        )
        porneste = st.button(
            t("sect.start"),
            key="afs_start",
            type="primary",
            use_container_width=True,
        )

    if porneste:
        with st.spinner(t("af.spinner")):
            try:
                elemente, model, nota = preia_din_teanc(
                    ("af", ctx.hash_material, dif, ctx.limba),
                    nr,
                    "intrebare",
                    lambda: genereaza_teanc_af(
                        ctx.client, ctx.selectate, ctx.eticheta, dif, ctx.limba
                    ),
                )
            except Exception as e_af:
                st.error(t("comun.eroare", e=e_af))
                return
        if not elemente:
            st.error(t("af.fara_elemente"))
            return
        info = f"{model} · {nota}"
        if len(elemente) < nr:
            info += t("af.doar_n", n=len(elemente))
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

    st.progress(i / total, text=t("af.progres", i=i + 1, total=total))
    st.caption(t("comun.model", info=s["info"]))

    st.markdown(
        '<div class="fc fc-mic">'
        f'<div class="fc-eticheta">{html.escape(t("af.intrebare"))}</div>'
        f'<div class="fc-text">{_html(q["intrebare"])}</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    if raspuns is None:
        b1, b2 = st.columns(2)
        b1.button(
            t("af.adevarat"),
            on_click=_raspunde,
            args=(0,),
            key="afs_adev",
            use_container_width=True,
        )
        b2.button(
            t("af.fals"),
            on_click=_raspunde,
            args=(1,),
            key="afs_fals",
            use_container_width=True,
        )
    else:
        if raspuns == q["corect"]:
            st.success(t("af.corect"))
        else:
            st.error(t("af.gresit", r=_var(q["corect"])))
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
            key="afs_next",
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
        salveaza_progres("af", scor, total)
        s["progres_salvat"] = True

    st.progress(1.0, text=t("sect.terminat"))
    c1, c2 = st.columns(2)
    c1.metric(t("sect.scor"), f"{scor}/{total}")
    c2.metric(t("sect.procent"), f"{procent}%")

    if not gresite:
        st.success(t("af.toate_corecte"))
    else:
        st.subheader(t("sect.recapitulezi"))
        grupuri = Counter(eticheta_grup_ui(q) for _, q in gresite)
        for eticheta, nr in grupuri.most_common():
            cuvant = t("af.afirmatie_gresita") if nr == 1 else t("af.afirmatii_gresite")
            st.markdown(t("sect.grup", eticheta=eticheta, n=nr, cuvant=cuvant))
        st.caption(t("af.nota"))
        with st.expander(t("af.vezi_gresite")):
            for i, q in gresite:
                ales = s["raspunsuri"].get(i)
                ales_text = _var(ales) if ales is not None else t("sect.fara_raspuns")
                st.markdown(f"**{i + 1}. {_md(q['intrebare'])}**")
                st.markdown(
                    t("sect.raspuns_tau_corect", x=ales_text, y=_var(q["corect"]))
                )
                if q.get("explicatie"):
                    st.caption(_md(q["explicatie"]))
                st.divider()

    st.download_button(
        t("af.descarca"),
        data=html_quiz(s["intrebari"]),
        file_name="adevarat_fals.html",
        mime="text/html",
        on_click="ignore",
        key="afs_dl",
    )
    b1, b2 = st.columns(2)
    if gresite:
        b1.button(
            t("af.repeta"),
            on_click=_repeta_gresite,
            key="afs_repeta",
            use_container_width=True,
        )
    b2.button(
        t("sect.nou"),
        on_click=_inceput_nou,
        key="afs_nou",
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
