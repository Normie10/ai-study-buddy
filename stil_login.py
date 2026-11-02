"""Stilul paginii de login, după poza de referință: stânga bun venit cu robotul,
dreapta cardul „Autentificare". Se încarcă doar de pe ecranele de login."""

# iconițele din câmpuri (desenate aici, fără fișiere)
_STIL_SVG = (
    "fill='none' stroke='%239A8FD8' stroke-width='1.8' "
    "stroke-linecap='round' stroke-linejoin='round'"
)
_IC_EMAIL = (
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' "
    f"viewBox='0 0 24 24' {_STIL_SVG}><rect x='3' y='5' width='18' height='14' rx='2.5'/>"
    "<path d='M3.5 7l8.5 6 8.5-6'/></svg>\")"
)
_IC_PAROLA = (
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' "
    f"viewBox='0 0 24 24' {_STIL_SVG}><rect x='5' y='11' width='14' height='9' rx='2.5'/>"
    "<path d='M8 11V8a4 4 0 0 1 8 0v3'/></svg>\")"
)

_CAMPURI = (
    'div[class*="st-key-login_"] [data-baseweb="input"]',
    'div[class*="st-key-reg_"] [data-baseweb="input"]',
    'div[class*="st-key-reset_"] [data-baseweb="input"]',
)
_CAMPURI_EMAIL = (
    'div[class*="st-key-login_email"] [data-baseweb="input"]',
    'div[class*="st-key-reg_email"] [data-baseweb="input"]',
    'div[class*="st-key-reset_email"] [data-baseweb="input"]',
)
_CAMPURI_PAROLA = (
    'div[class*="st-key-login_parola"] [data-baseweb="input"]',
    'div[class*="st-key-reg_parola"] [data-baseweb="input"]',
)

CSS_LOGIN = (
    "<style>"
    + """
/* marca roșie veche de la ecranele cu antet, în violet */
.hero-marca {
    background: linear-gradient(180deg, #8B5CF6 0%, #5B34C2 100%) !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.45) !important;
}

.log-marker { display: none; }
[data-testid="stMainBlockContainer"]:has(.log-marker) {
    max-width: 1180px !important;
    padding-top: 2.2rem !important;
}
/* pe login nu are rost butonul de mod: pagina e mereu întunecată */
body:has(.log-marker) div[class*="st-key-comutator_mod"] { display: none !important; }
[data-testid="stApp"]:has(.log-marker) {
    background-image:
        radial-gradient(760px 520px at 12% 95%, rgba(109, 74, 224, 0.30), transparent 62%),
        radial-gradient(700px 520px at 100% 0%, rgba(139, 92, 246, 0.20), transparent 60%) !important;
}

/* ---------- stânga: marca, titlul, robotul ---------- */
.log-stanga {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-top: 0.5rem;
}
.log-brand { align-self: flex-start; display: flex; align-items: center; gap: 0.9rem; }
.log-logo { width: 58px; height: auto; }
.log-brand-nume { font-size: 1.35rem; font-weight: 800; line-height: 1.15; text-align: left; }
.log-brand-nume b { color: #A78BFA; }
.log-titlu {
    margin-top: 2.6rem;
    font-size: clamp(2.2rem, 3.6vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.12;
}
.log-titlu span {
    background: linear-gradient(90deg, #8B5CF6, #B79BFF);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.log-sub {
    max-width: 30rem;
    margin-top: 1rem;
    color: #D6D3EA;
    font-size: 1.05rem;
    line-height: 1.5;
}
.log-robot { width: 100%; max-width: 560px; height: auto; margin-top: 1.2rem; }

/* ---------- dreapta: cardul ---------- */
div[class*="st-key-log_card"] {
    padding: 2.2rem 2.4rem 1.8rem;
    border: 1px solid rgba(139, 92, 246, 0.45);
    border-radius: 26px;
    background: linear-gradient(180deg, rgba(34, 27, 74, 0.55), rgba(14, 11, 32, 0.78));
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.5);
}
.log-card-cap { display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 1.2rem; }
.log-card-logo { width: 74px; height: auto; }
.log-card-titlu { margin-top: 0.7rem; font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }
.log-card-sub { margin-top: 0.35rem; color: #CFCCE6; font-size: 1rem; }

div[class*="st-key-log_card"] [data-testid="stForm"] {
    border: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}
div[class*="st-key-log_card"] [data-baseweb="input"] {
    min-height: 3.2rem;
    border-radius: 14px !important;
    border: 1px solid rgba(139, 92, 246, 0.40) !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
}
div[class*="st-key-log_card"] [data-baseweb="input"] input {
    padding-left: 3rem !important;
    font-size: 1rem;
}
"""
    + ",\n".join(_CAMPURI)
    + " { position: relative; }\n"
    + ",\n".join(f"{s}::before" for s in _CAMPURI)
    + """ {
    content: "";
    position: absolute;
    left: 14px;
    top: 50%;
    width: 22px;
    height: 22px;
    transform: translateY(-50%);
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    pointer-events: none;
    z-index: 2;
}
"""
    + ",\n".join(f"{s}::before" for s in _CAMPURI_EMAIL)
    + " { background-image: " + _IC_EMAIL + "; }\n"
    + ",\n".join(f"{s}::before" for s in _CAMPURI_PAROLA)
    + " { background-image: " + _IC_PAROLA + "; }\n"
    + """
/* butonul de intrare: violet spre roz, pe toată lățimea */
div[class*="st-key-log_card"] button[data-testid="stBaseButton-primaryFormSubmit"],
div[class*="st-key-log_card"] button[data-testid="baseButton-primaryFormSubmit"] {
    min-height: 3.2rem;
    margin-top: 0.4rem;
    border: 0 !important;
    border-radius: 14px !important;
    background: linear-gradient(90deg, #6D4AE0 0%, #D96BEA 100%) !important;
    font-size: 1.05rem;
}
div[class*="st-key-log_card"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
div[class*="st-key-log_card"] button[data-testid="baseButton-primaryFormSubmit"]:hover {
    filter: brightness(1.08);
}

/* „sau" cu linii de o parte și de alta */
.log-sau {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 1.1rem 0 0.9rem;
    color: #9D9AB6;
    font-size: 0.9rem;
}
.log-sau::before, .log-sau::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(139, 92, 246, 0.30);
}

/* „Continuă fără cont": buton cu margine, ca „Continuă cu Google" din poză */
div[class*="st-key-log_oaspete"] button {
    min-height: 3.2rem;
    border-radius: 14px !important;
    border: 1px solid rgba(139, 92, 246, 0.45) !important;
    background: rgba(255, 255, 255, 0.02) !important;
    font-size: 1rem;
}
.log-mic { margin-top: 0.5rem; color: #9D9AB6; font-size: 0.82rem; text-align: center; }

/* „Nu ai cont? Creează unul acum →" și „Ai uitat parola?": ca niște legături */
div[class*="st-key-log_alt"] button,
div[class*="st-key-log_uitat"] button {
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #B79BFF !important;
    font-weight: 600;
}
div[class*="st-key-log_alt"] button { font-size: 1rem; }
div[class*="st-key-log_uitat"] button { font-size: 0.9rem; }
div[class*="st-key-log_alt"], div[class*="st-key-log_uitat"] {
    display: flex;
    justify-content: center;
}
div[class*="st-key-log_card"] [data-testid="stRadio"] label p { font-size: 0.88rem; }

@media (max-width: 900px) {
    .log-robot { display: none; }
    .log-titlu { margin-top: 1.4rem; }
    div[class*="st-key-log_card"] { padding: 1.6rem 1.3rem 1.3rem; }
}
"""
    + "</style>"
)
