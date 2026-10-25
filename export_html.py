"""Fișierele HTML pe care le descarci și le printezi (quiz, flashcarduri, rezultate).

Etichetele documentului urmează limba interfeței; întrebările, variantele și
cuvintele Adevărat/Fals urmează limba întrebărilor."""

from html import escape as esc

from limbi import limba_ui, sursa_ui, t, text_intrebare_ui, unitate_sg, varianta_ui
from utile import formateaza_timp

CSS_PRINT = """
body { font-family: Arial, Helvetica, sans-serif; max-width: 800px;
       margin: 24px auto; padding: 0 16px; color: #111; line-height: 1.5; }
h1 { font-size: 24px; margin-bottom: 4px; }
h2 { font-size: 18px; margin-top: 28px; }
.intrebare { margin: 16px 0; page-break-inside: avoid; }
.intrebare p { margin: 0 0 6px 0; font-weight: bold; }
.varianta { margin: 2px 0 2px 18px; }
.pasaj { border-left: 3px solid #888; padding: 4px 10px; margin: 6px 0; color: #222; }
.cheie { page-break-before: always; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #888; padding: 8px; vertical-align: top; text-align: left; }
th { background: #eee; }
tr { page-break-inside: avoid; }
.ok { color: #136f2b; }
.gresit { color: #b00020; }
.mic { color: #555; font-size: 13px; }
.nu-print { padding: 8px 14px; margin-bottom: 16px; font-size: 14px; cursor: pointer; }
@media print {
  .nu-print { display: none; }
  body { margin: 0; max-width: none; }
}
"""

# Formulele de la Math se afișează cu MathJax (are nevoie de internet)
MATHJAX = """<script>window.MathJax = {tex: {inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], processEscapes: true}};</script>
<script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js"></script>"""


def e(valoare, q=None):
    """Escapare pentru HTML (ca textul din document să nu strice pagina)."""
    text = esc(str(valoare))
    if q is not None and q.get("tip") == "rw":
        text = text.replace("$", "\\$")
    return text


def html_pagina(titlu, corp, mathjax=False):
    extra = MATHJAX if mathjax else ""
    return f"""<!DOCTYPE html>
<html lang="{limba_ui()}">
<head>
<meta charset="utf-8">
<title>{e(titlu)}</title>
<style>{CSS_PRINT}</style>
{extra}
</head>
<body>
<button class="nu-print" onclick="window.print()">{e(t("exp.print"))}</button>
<h1>{e(titlu)}</h1>
{corp}
</body>
</html>"""


def html_quiz(quiz):
    litere = "ABCD"
    parti = [f'<p class="mic">{t("exp.nume_data")}</p>']
    for i, q in enumerate(quiz, start=1):
        parti.append('<div class="intrebare">')
        parti.append(f"<p>{i}. {e(text_intrebare_ui(q))}</p>")
        for j, v in enumerate(q["variante"]):
            afisat = e(varianta_ui(v, q))
            if q.get("tip_intrebare") == "af":
                parti.append(f'<div class="varianta">&#9744; {afisat}</div>')
            else:
                parti.append(f'<div class="varianta">&#9744; {litere[j]}. {afisat}</div>')
        parti.append("</div>")

    parti.append(f'<div class="cheie"><h2>{e(t("exp.raspunsuri_corecte"))}</h2>')
    for i, q in enumerate(quiz, start=1):
        corect = q["corect"]
        text_corect = varianta_ui(q["variante"][corect], q)
        if q.get("tip_intrebare") == "af":
            raspuns = text_corect
        else:
            raspuns = f"{litere[corect]}. {text_corect}"
        parti.append(
            f"<p>{i}. <b>{e(raspuns)}</b> "
            f"<span class=\"mic\">({e(sursa_ui(q))}) "
            f"{e(q['explicatie'])}</span></p>"
        )
    parti.append("</div>")
    return html_pagina(t("exp.titlu_quiz"), "\n".join(parti))


def html_carduri(carduri):
    randuri = [
        f"<table><tr><th>#</th><th>{e(t('exp.col_intrebare'))}</th>"
        f"<th>{e(t('exp.col_raspuns'))}</th><th>{e(t('exp.col_sursa'))}</th></tr>"
    ]
    for i, c in enumerate(carduri, start=1):
        sursa = f"{unitate_sg(c.get('unitate', 'pagina'))} {c.get('pagina', '?')}"
        randuri.append(
            f"<tr><td>{i}</td><td>{e(c['fata'])}</td>"
            f"<td>{e(c['spate'])}</td>"
            f"<td>{e(sursa)}</td></tr>"
        )
    randuri.append("</table>")
    return html_pagina(t("exp.titlu_carduri"), "\n".join(randuri))


def _titlu_ui(titlu):
    """Titlul testului e păstrat în română în sesiune (valoare internă); aici îl
    afișăm în limba interfeței. Titlurile necunoscute rămân cum sunt."""
    titlu = str(titlu)
    prefix_recap = "Recapitulare greșeli - "
    if titlu.startswith(prefix_recap):
        return t("exp.titlu_recap", titlu=_titlu_ui(titlu[len(prefix_recap):]))
    prefix_sat = "Rezultate SAT - "
    if titlu.startswith(prefix_sat):
        return t("exp.titlu_sat", sectiune=titlu[len(prefix_sat):])
    if titlu == "Rezultate examen":
        return t("exp.titlu_examen")
    return titlu


def html_examen(titlu, scor, total, procent, folosit, de_recapitulat, detalii, mathjax):
    parti = [
        "<p>"
        + t(
            "exp.scor_timp",
            scor=scor,
            total=total,
            procent=procent,
            timp=formateaza_timp(folosit),
        )
        + "</p>",
        f"<h2>{e(t('exp.ce_recapitulezi'))}</h2>",
    ]
    if not de_recapitulat:
        parti.append(f"<p>{e(t('exp.toate_corecte'))}</p>")
    else:
        parti.append("<ul>")
        for eticheta, tot, g in de_recapitulat:
            parti.append(
                "<li>"
                + t("exp.grup_gresite", eticheta=e(eticheta), g=g, tot=tot)
                + "</li>"
            )
        parti.append("</ul>")

    parti.append(f"<h2>{e(t('exp.intrebarile'))}</h2>")
    for i, q, ales, ok in detalii:
        clasa = "ok" if ok else "gresit"
        stare = t("exp.corect") if ok else t("exp.gresit")
        parti.append('<div class="intrebare">')
        if q.get("pasaj"):
            pasaj_html = e(q["pasaj"], q).replace("\n", "<br>")
            parti.append(f'<div class="pasaj">{pasaj_html}</div>')
        parti.append(
            f'<p class="{clasa}">{i + 1}. {e(text_intrebare_ui(q), q)} '
            f'<span class="mic">({e(stare)})</span></p>'
        )
        raspuns_tau = (
            e(varianta_ui(ales, q), q) if ales else e(t("exp.fara_raspuns"))
        )
        parti.append(f"<div>{t('exp.raspunsul_tau', r=raspuns_tau)}</div>")
        if not ok:
            corect_txt = e(varianta_ui(q["variante"][q["corect"]], q), q)
            parti.append(f"<div>{t('exp.raspuns_corect', r=corect_txt)}</div>")
        explicatie = e(q["explicatie"], q).replace("\n", "<br>")
        parti.append(f'<div class="mic">{explicatie} ({e(sursa_ui(q))})</div>')
        parti.append("</div>")
    return html_pagina(_titlu_ui(titlu), "\n".join(parti), mathjax=mathjax)
