"""Secțiune: Potrivește perechile.

Cardurile (flashcardurile) din materialul tău, amestecate: legi fiecare
termen sau întrebare de răspunsul lui. Folosește același teanc de carduri ca
secțiunea Flashcarduri, deci nu cere nimic în plus la Google dacă ai generat
deja cardurile.
"""

import random

import streamlit as st

from baza_date import salveaza_progres
from generare import genereaza_teanc_carduri
from limbi import descriere_sectiune, t
from memorie import preia_din_teanc
from stil_sectiuni import injecteaza_stiluri
from utile import norm

NUME = "Potrivește perechile"
ORDINE = 28
CERE_MATERIAL = True
DESCRIERE = (
    "Legi fiecare termen sau întrebare de răspunsul lui, folosind cardurile "
    "din materialul tău. Alegi un element din stânga, apoi răspunsul din dreapta."
)

CHEIE = "pp_sesiune"
MIN_PERECHI = 4
MAX_PERECHI = 10


def _eticheta(text):
    """Text pentru un buton: pe un singur rând, cu $ protejat."""
    return " ".join(str(text).split()).replace("$", "\\$")


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _unice(elemente, nr):
    """Alege cel mult nr perechi la care nici fața, nici spatele nu se repetă
    (altfel două răspunsuri identice ar încurca potrivirea)."""
    vazute, perechi = set(), []
    for e in elemente:
        fata = " ".join(str(e.get("fata", "")).split())
        spate = " ".join(str(e.get("spate", "")).split())
        if not fata or not spate:
            continue
        cf, cs = norm(fata), norm(spate)
        if cf == cs or cf in vazute or cs in vazute:
            continue
        vazute.add(cf)
        vazute.add(cs)
        perechi.append({"fata": fata, "spate": spate})
        if len(perechi) >= nr:
            break
    return perechi


def _porneste(perechi, info, hash_material):
    ordine = list(range(len(perechi)))
    random.shuffle(ordine)
    if len(ordine) > 1 and ordine == sorted(ordine):
        random.shuffle(ordine)
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "perechi": perechi,
        "info": info,
        "ordine": ordine,  # ordinea răspunsurilor în coloana din dreapta
        "sel": None,  # elementul ales în stânga
        "potrivite": [],
        "gresite": {},  # pereche -> de câte ori am greșit
        "ultimul": None,  # "ok" / "gresit" / None
        "progres_salvat": False,
    }


def _alege_stanga(i):
    s = st.session_state.get(CHEIE)
    if s and i not in s["potrivite"]:
        s["sel"] = i
        s["ultimul"] = None


def _alege_dreapta(j):
    s = st.session_state.get(CHEIE)
    if not s or s["sel"] is None or j in s["potrivite"]:
        return
    i = s["sel"]
    if i == j:
        s["potrivite"].append(i)
        s["ultimul"] = "ok"
    else:
        s["gresite"][i] = s["gresite"].get(i, 0) + 1
        s["ultimul"] = "gresit"
    s["sel"] = None


def _inceput_nou():
    st.session_state.pop(CHEIE, None)


def _repeta_gresite():
    s = st.session_state.get(CHEIE)
    if not s:
        return
    ids = sorted(s["gresite"].keys())
    if len(ids) >= 2:
        _porneste([s["perechi"][i] for i in ids], s["info"], s["hash"])


def _setari(ctx):
    with st.container(border=True):
        nr = st.number_input(
            t("pp.nr"), MIN_PERECHI, MAX_PERECHI, 6, key="pp_nr"
        )
        porneste = st.button(
            t("sect.start"),
            key="pp_start",
            type="primary",
            use_container_width=True,
        )

    if porneste:
        with st.spinner(t("fc.spinner")):
            try:
                elemente, model, nota = preia_din_teanc(
                    ("carduri", ctx.hash_material, ctx.limba),
                    nr + 2,
                    "fata",
                    lambda: genereaza_teanc_carduri(
                        ctx.client, ctx.selectate, ctx.eticheta, ctx.limba
                    ),
                )
            except Exception as e_pp:
                st.error(t("comun.eroare", e=e_pp))
                return
        perechi = _unice(elemente, nr)
        if len(perechi) < MIN_PERECHI:
            st.error(t("pp.putine"))
            return
        _porneste(perechi, f"{model} · {nota}", ctx.hash_material)
        st.rerun()


def _joc(s):
    perechi = s["perechi"]
    total = len(perechi)
    potrivite = s["potrivite"]

    st.progress(
        len(potrivite) / total,
        text=t("pp.progres", i=len(potrivite), total=total),
    )
    st.caption(t("comun.model", info=s["info"]))
    st.caption(t("pp.instructiuni"))

    if s["ultimul"] == "ok":
        st.success(t("pp.ok"))
    elif s["ultimul"] == "gresit":
        st.error(t("pp.gresit"))

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{t('pp.termeni')}**")
        for i, p in enumerate(perechi):
            gata = i in potrivite
            st.button(
                _eticheta(p["fata"]),
                key=f"pp_s_{i}",
                on_click=_alege_stanga,
                args=(i,),
                disabled=gata,
                type="primary" if s["sel"] == i else "secondary",
                icon=":material/check:" if gata else None,
                use_container_width=True,
            )
    with c2:
        st.markdown(f"**{t('pp.raspunsuri')}**")
        for j in s["ordine"]:
            gata = j in potrivite
            st.button(
                _eticheta(perechi[j]["spate"]),
                key=f"pp_d_{j}",
                on_click=_alege_dreapta,
                args=(j,),
                disabled=gata or s["sel"] is None,
                icon=":material/check:" if gata else None,
                use_container_width=True,
            )

    st.button(
        t("sect.nou"),
        on_click=_inceput_nou,
        key="pp_nou_joc",
        use_container_width=True,
    )


def _rezultate(s):
    perechi = s["perechi"]
    total = len(perechi)
    cu_greseli = sorted(s["gresite"].keys())
    scor = total - len(cu_greseli)
    procent = round(100 * scor / total)

    if not s.get("progres_salvat"):
        salveaza_progres("perechi", scor, total)
        s["progres_salvat"] = True

    st.progress(1.0, text=t("sect.terminat"))
    m1, m2, m3 = st.columns(3)
    m1.metric(t("sect.scor"), f"{scor}/{total}")
    m2.metric(t("sect.procent"), f"{procent}%")
    m3.metric(t("pp.greseli"), sum(s["gresite"].values()))

    if not cu_greseli:
        st.success(t("pp.toate_prima"))
    else:
        st.subheader(t("pp.dificile"))
        for i in cu_greseli:
            p = perechi[i]
            st.markdown(
                "- " + t("pp.perechea", x=_md(p["fata"]), y=_md(p["spate"]))
            )

    b1, b2 = st.columns(2)
    if len(cu_greseli) >= 2:
        b1.button(
            t("pp.repeta"),
            on_click=_repeta_gresite,
            key="pp_repeta",
            use_container_width=True,
        )
    b2.button(
        t("sect.nou"),
        on_click=_inceput_nou,
        key="pp_nou",
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
    elif len(s["potrivite"]) < len(s["perechi"]):
        _joc(s)
    else:
        _rezultate(s)
