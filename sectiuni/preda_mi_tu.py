"""Secțiune: Predă-mi tu.

Alegi un subiect din material și îl explici unui coleg AI. Colegul pune
întrebări. Când te oprești (sau când se atinge limita de mesaje), primești o
părere cu note pe categorii, comparată cu documentul.
"""

from pathlib import Path

import streamlit as st

from baza_date import salveaza_progres
from documente import alege_fragmente
from generare_preda import CATEGORII, evalueaza_explicatia, raspunde_coleg
from limbi import descriere_sectiune, t
from stil_sectiuni import injecteaza_stiluri

NUME = "Predă-mi tu"
ORDINE = 65
CERE_MATERIAL = True
DESCRIERE = (
    "Alegi un subiect din material și îl explici unui coleg AI, cu cuvintele "
    "tale. Colegul pune întrebări, iar când te oprești primești o părere cu "
    "note pe categorii."
)

CHEIE = "pt_sesiune"
MAX_MESAJE = 20  # mesajele TALE; după ele se oprește singur și primești nota
MAX_LUNGIME_MESAJ = 1500
MAX_LUNGIME_SUBIECT = 120
SCOR_MAXIM = 100

_FISIER_AVATAR = Path(__file__).resolve().parent.parent / "avatar_coleg.png"
AVATAR = str(_FISIER_AVATAR) if _FISIER_AVATAR.exists() else None


def _md(text):
    """Semnul $ nu trebuie interpretat ca formulă."""
    return str(text).replace("$", "\\$")


def _porneste(subiect, hash_material):
    st.session_state[CHEIE] = {
        "hash": hash_material,
        "subiect": subiect,
        "mesaje": [],  # {"rol": "user" / "assistant", "text": ...}
        "trimise": 0,  # câte mesaje ale elevului s-au trimis
        "rezultat": None,
        "model_nota": "",
        "progres_salvat": False,
    }


def _inceput_nou():
    st.session_state.pop(CHEIE, None)


def _setari(ctx):
    st.markdown(t("pt.intro"))
    with st.container(border=True):
        subiect = st.text_input(
            t("pt.subiect"),
            max_chars=MAX_LUNGIME_SUBIECT,
            placeholder=t("pt.subiect.placeholder"),
            key="pt_subiect",
        )
        porneste = st.button(
            t("sect.start"),
            key="pt_start",
            type="primary",
            use_container_width=True,
        )
    if porneste:
        subiect = subiect.strip()
        if len(subiect) < 3:
            st.warning(t("pt.subiect_scurt"))
            return
        _porneste(subiect, ctx.mat["hash"])
        st.rerun()


def _termina(ctx, s):
    """Cere nota de la model și o salvează în progres (o singură dată).
    Întoarce True dacă a reușit."""
    text_elev = " ".join(m["text"] for m in s["mesaje"] if m["rol"] == "user")
    with st.spinner(t("pt.spinner_nota")):
        try:
            fragmente, partial = alege_fragmente(
                ctx.mat, s["subiect"], text_elev[:1500]
            )
            rezultat, model = evalueaza_explicatia(
                ctx.client,
                fragmente,
                ctx.eticheta,
                partial,
                s["subiect"],
                s["mesaje"],
                ctx.limba,
            )
        except Exception as e_nota:
            st.error(t("comun.eroare", e=e_nota))
            return False
    s["rezultat"] = rezultat
    s["model_nota"] = model
    if not s.get("progres_salvat"):
        salveaza_progres("preda", rezultat["scor"], SCOR_MAXIM)
        s["progres_salvat"] = True
    return True


def _chat(ctx, s):
    st.caption(t("pt.tema", subiect=s["subiect"]))
    contor = st.empty()
    zona_chat = st.container()

    mesaj = ""
    trimis = False
    if s["trimise"] < MAX_MESAJE:
        with st.form("form_preda", clear_on_submit=True):
            mesaj = st.text_area(
                t("pt.eticheta"),
                height=140,
                max_chars=MAX_LUNGIME_MESAJ,
                placeholder=t("pt.placeholder"),
            )
            trimis = st.form_submit_button(t("pt.trimite"))
    else:
        st.info(t("pt.limita"))

    termina = False
    if trimis and mesaj.strip():
        mesaj = mesaj.strip()
        if s["trimise"] + 1 >= MAX_MESAJE:
            # ultimul mesaj permis: nu mai cerem replică, trecem direct la notă
            s["mesaje"].append({"rol": "user", "text": mesaj})
            s["trimise"] += 1
            termina = True
        else:
            with st.spinner(t("pt.spinner_coleg")):
                try:
                    raspuns, _model = raspunde_coleg(
                        ctx.client, s["subiect"], s["mesaje"], mesaj, ctx.limba
                    )
                    s["mesaje"].append({"rol": "user", "text": mesaj})
                    s["mesaje"].append({"rol": "assistant", "text": raspuns})
                    s["trimise"] += 1
                except Exception as e_pt:
                    st.error(t("comun.eroare", e=e_pt))
                    with st.expander(t("pt.text_pierdut"), expanded=True):
                        st.code(mesaj, language=None)

    if termina and _termina(ctx, s):
        st.rerun()

    contor.caption(t("pt.ramase", n=max(MAX_MESAJE - s["trimise"], 0)))

    with zona_chat:
        with st.chat_message("assistant", avatar=AVATAR):
            st.markdown(t("pt.salut", subiect=_md(s["subiect"])))
        for m in s["mesaje"]:
            if m["rol"] == "assistant":
                with st.chat_message("assistant", avatar=AVATAR):
                    st.markdown(_md(m["text"]))
            else:
                with st.chat_message("user"):
                    st.markdown(_md(m["text"]))

    if st.button(t("pt.stop"), key="pt_stop", use_container_width=True):
        if not s["mesaje"]:
            st.warning(t("pt.nimic"))
        elif _termina(ctx, s):
            st.rerun()


def _lista(titlu, elemente):
    if elemente:
        st.subheader(titlu)
        for e in elemente:
            st.markdown("- " + _md(e))


def _rezultat(s):
    r = s["rezultat"]
    st.progress(1.0, text=t("sect.terminat"))
    c1, c2 = st.columns(2)
    c1.metric(t("pt.nota"), f"{r['scor']}/{SCOR_MAXIM}")
    c2.metric(t("pt.mesaje_trimise"), f"{s['trimise']}/{MAX_MESAJE}")
    st.caption(t("pt.avertisment"))
    if s.get("model_nota"):
        st.caption(t("comun.model", info=s["model_nota"]))

    st.subheader(t("pt.categorii"))
    for cod in CATEGORII:
        eticheta = t(f"pt.cat.{cod}")
        valoare = r.get(cod)
        if valoare is None:
            st.caption(f"{eticheta}: {t('pt.nu_se_aplica')}")
        else:
            st.progress(valoare / 10, text=f"{eticheta}: {valoare}/10")

    _lista(t("pt.acoperite"), r["acoperite"])
    _lista(t("pt.omise"), r["omise"])
    if r["greseli"]:
        st.subheader(t("pt.greseli"))
        for g in r["greseli"]:
            st.markdown(
                "- "
                + t(
                    "pt.greseala",
                    x=_md(g["a_spus"]),
                    y=_md(g["documentul_spune"]),
                )
            )
    _lista(t("pt.sfaturi"), r["sfaturi"])

    st.button(
        t("sect.nou"),
        on_click=_inceput_nou,
        key="pt_nou",
        use_container_width=True,
    )


def afiseaza(ctx):
    """Funcția pe care o apelează aplicația pentru această secțiune."""
    injecteaza_stiluri()
    st.caption(descriere_sectiune(NUME, DESCRIERE))

    s = st.session_state.get(CHEIE)
    if s and s["hash"] != ctx.mat["hash"]:
        st.session_state.pop(CHEIE, None)  # s-a schimbat documentul
        s = None

    if s is None:
        _setari(ctx)
    elif s["rezultat"] is None:
        _chat(ctx, s)
    else:
        _rezultat(s)
