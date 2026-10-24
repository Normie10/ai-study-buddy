"""Prototipul paginii de abonamente: două planuri (Gratuit și Premium), pe o
pagină separată, care se deschide din meniul de profil. Nu există plată
reală, iar limitele afișate nu sunt încă aplicate în aplicație."""

import html

import streamlit as st

from baza_date import _client, iese_din_mod_vizitator, utilizator_curent
from limbi import t

PLANURI = ("gratuit", "premium")
NR_AVANTAJE = 6

# Cheile "Lunar" / "Anual" sunt valori interne (nu se traduc); textele din
# dreapta sunt chei de traducere.
PRETURI = {
    "Lunar": {"suma": "19", "unit": "abon_unit_lunar", "sub": "abon_sub_lunar"},
    "Anual": {"suma": "149", "unit": "abon_unit_anual", "sub": "abon_sub_anual"},
}
PRET_GRATUIT = {"suma": "0", "unit": "abon_unit_gratuit", "sub": "abon_sub_gratuit"}

CSS_ABONAMENTE = """
<style>
.abon-antet {
    margin: 0.5rem 0 0.9rem;
}
.abon-titlu {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.1;
}
.abon-sub {
    margin-top: 0.35rem;
    color: var(--muted);
    font-size: 0.95rem;
}
.abon-prototip {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.9rem;
    color: var(--muted);
    font-size: 0.85rem;
}
.abon-pastila {
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.planuri {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem;
    margin: 0.5rem 0 0.75rem;
}
.plan {
    display: flex;
    flex-direction: column;
    padding: 1.2rem 1.25rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--surface);
    transition: border-color 0.2s ease;
}
.plan:hover {
    border-color: var(--border-hover);
}
.plan-premium {
    border-color: rgba(229, 56, 59, 0.55);
    background: linear-gradient(
        180deg, rgba(229, 56, 59, 0.08), rgba(229, 56, 59, 0.02)
    );
    box-shadow: 0 12px 32px rgba(229, 56, 59, 0.12);
}
.plan-premium:hover {
    border-color: var(--accent);
}
.plan-cap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    min-height: 1.6rem;
}
.plan-nume {
    font-size: 1.05rem;
    font-weight: 700;
}
.plan-eticheta {
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    background: var(--accent);
    color: #FFFFFF;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.plan-eticheta-curent {
    background: transparent;
    border: 1px solid var(--border-hover);
    color: var(--muted);
}
.plan-pret {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    margin-top: 0.7rem;
}
.plan-suma {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
}
.plan-unit {
    color: var(--muted);
    font-size: 0.85rem;
    font-weight: 600;
}
.plan-sub {
    min-height: 1.2rem;
    margin-top: 0.3rem;
    color: var(--muted);
    font-size: 0.82rem;
}
.plan-lista {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin: 1rem 0 0;
    padding: 1rem 0 0;
    border-top: 1px solid var(--border);
    list-style: none;
}
.plan-lista li {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    font-size: 0.9rem;
    line-height: 1.4;
}
.plan-lista li::before {
    content: "";
    flex-shrink: 0;
    width: 16px;
    height: 16px;
    margin-top: 0.15rem;
    background: var(--accent);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-size: contain;
    mask-size: contain;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
}
/* Butoanele dezactivate (planul actual): vizibile, dar liniștite */
[class*="st-key-abon_"] button:disabled {
    background: transparent !important;
    border: 1px solid var(--border-hover) !important;
    color: var(--muted) !important;
    box-shadow: none !important;
    opacity: 1 !important;
}
.st-key-abon_premium_curent button:disabled {
    border-color: rgba(229, 56, 59, 0.5) !important;
    color: var(--accent) !important;
}
@media (max-width: 640px) {
    .planuri { grid-template-columns: 1fr; }
}
</style>
"""


def nume_plan(plan):
    """Numele afișat al unui plan (în limba interfeței)."""
    return t(f"abon_plan_{plan}")


# ------------------------- planul ales -------------------------
def plan_curent():
    """Planul ales de utilizator. Vizitatorii sunt mereu pe planul Gratuit."""
    user = utilizator_curent()
    if user is None:
        return "gratuit"
    din_sesiune = st.session_state.get("plan_sesiune")
    if din_sesiune and din_sesiune[0] == user.id:
        return din_sesiune[1]
    meta = getattr(user, "user_metadata", None) or {}
    plan = meta.get("plan_demo")
    return plan if plan in PLANURI else "gratuit"


def seteaza_plan(plan):
    """Salvează planul în datele contului. Întoarce True dacă s-a salvat pe
    cont, False dacă a rămas doar în sesiunea curentă."""
    user = utilizator_curent()
    if user is None or plan not in PLANURI:
        return False
    st.session_state["plan_sesiune"] = (user.id, plan)
    try:
        rezultat = _client().auth.update_user({"data": {"plan_demo": plan}})
        if rezultat is not None and rezultat.user is not None:
            st.session_state["utilizator"] = rezultat.user
        return True
    except Exception:
        return False


def _alege_plan(plan):
    st.session_state["plan_doar_sesiune"] = not seteaza_plan(plan)


# ------------------------- deschidere / închidere pagină -------------------------
def deschide_abonamente():
    st.session_state["pagina_abonamente"] = True
    st.rerun()


def inchide_abonamente():
    st.session_state.pop("pagina_abonamente", None)


# ------------------------- aspect -------------------------
def _card_html(plan, curent, facturare):
    pret = PRETURI[facturare] if plan == "premium" else PRET_GRATUIT

    if plan == curent:
        text_eticheta = html.escape(t("abon_eticheta_curent"))
        eticheta = (
            '<span class="plan-eticheta plan-eticheta-curent">'
            f"{text_eticheta}</span>"
        )
    elif plan == "premium":
        text_eticheta = html.escape(t("abon_eticheta_recomandat"))
        eticheta = f'<span class="plan-eticheta">{text_eticheta}</span>'
    else:
        eticheta = ""

    clasa = "plan plan-premium" if plan == "premium" else "plan"
    avantaje = [t(f"abon_av_{plan}_{n}") for n in range(1, NR_AVANTAJE + 1)]
    lista = "".join(f"<li>{html.escape(text)}</li>" for text in avantaje)
    unitate = html.escape(t(pret["unit"]))
    sub = html.escape(t(pret["sub"]))
    # totul pe un singur rând, fără linii goale, altfel Markdown strică HTML-ul
    return (
        f'<div class="{clasa}">'
        f'<div class="plan-cap"><span class="plan-nume">'
        f"{html.escape(nume_plan(plan))}</span>"
        f"{eticheta}</div>"
        f'<div class="plan-pret"><span class="plan-suma">{pret["suma"]}</span>'
        f'<span class="plan-unit">{unitate}</span></div>'
        f'<div class="plan-sub">{sub}</div>'
        f'<ul class="plan-lista">{lista}</ul>'
        "</div>"
    )


def afiseaza_pagina_abonamente():
    """Pagina de abonamente. Înlocuiește tot restul paginii, inclusiv meniul
    de profil (așa nu poate rămâne deschis peste ea)."""
    st.markdown(CSS_ABONAMENTE, unsafe_allow_html=True)

    if st.button(
        t("abon_inapoi"), key="abon_inapoi", icon=":material/arrow_back:"
    ):
        inchide_abonamente()
        st.rerun()

    st.markdown(
        '<div class="abon-antet">'
        f'<div class="abon-titlu">{html.escape(t("abon_pagina_titlu"))}</div>'
        f'<div class="abon-sub">{html.escape(t("abon_pagina_sub"))}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="abon-prototip">'
        f'<span class="abon-pastila">{html.escape(t("abon_prototip_pastila"))}</span>'
        f'{html.escape(t("abon_prototip_text"))}</div>',
        unsafe_allow_html=True,
    )

    facturare = st.radio(
        t("abon_facturare_eticheta"),
        ["Lunar", "Anual"],
        horizontal=True,
        key="abon_facturare",
        label_visibility="collapsed",
        format_func=lambda v: (
            t("abon_fact_lunar") if v == "Lunar" else t("abon_fact_anual")
        ),
    )
    curent = plan_curent()
    st.markdown(
        '<div class="planuri">'
        + _card_html("gratuit", curent, facturare)
        + _card_html("premium", curent, facturare)
        + "</div>",
        unsafe_allow_html=True,
    )

    este_cont = utilizator_curent() is not None
    c1, c2 = st.columns(2)
    with c1:
        if curent == "gratuit":
            st.button(
                t("abon_btn_gratuit_curent"),
                key="abon_gratuit_curent",
                disabled=True,
                use_container_width=True,
            )
        else:
            st.button(
                t("abon_btn_treci_gratuit"),
                key="abon_treci_gratuit",
                on_click=_alege_plan,
                args=("gratuit",),
                use_container_width=True,
            )
    with c2:
        if not este_cont:
            if st.button(
                t("abon_btn_cont"),
                key="abon_cont_nou",
                type="primary",
                use_container_width=True,
            ):
                iese_din_mod_vizitator()
                inchide_abonamente()
                st.rerun()
        elif curent == "premium":
            st.button(
                t("abon_btn_premium_activ"),
                key="abon_premium_curent",
                disabled=True,
                use_container_width=True,
            )
        else:
            st.button(
                t("abon_btn_alege_premium"),
                key="abon_alege_premium",
                on_click=_alege_plan,
                args=("premium",),
                type="primary",
                use_container_width=True,
            )

    if st.session_state.get("plan_doar_sesiune"):
        st.warning(t("abon_doar_sesiune"))
    st.caption(t("abon_nota"))


# ------------------------- intrări în meniul de profil -------------------------
def antet_profil(email):
    """Înlocuiește linia cu emailul din meniul de profil: email, planul curent
    și butonul care deschide pagina de abonamente."""
    st.write(f"**{email}**")
    st.caption(t("abon_profil_plan", plan=nume_plan(plan_curent())))
    if st.button(
        t("abon_profil_btn"),
        key="profil_abonamente",
        icon=":material/workspace_premium:",
        use_container_width=True,
    ):
        deschide_abonamente()


def butoane_vizitator():
    """Pentru vizitatori: butonul de planuri, apoi „Creează cont”. Întoarce
    True dacă s-a apăsat „Creează cont”."""
    if st.button(
        t("abon_viz_planuri"),
        key="profil_planuri_viz",
        icon=":material/workspace_premium:",
        use_container_width=True,
    ):
        deschide_abonamente()
    return st.button(
        t("abon_viz_cont"), key="profil_creeaza_cont", use_container_width=True
    )
