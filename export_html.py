"""Fișierele HTML pe care le descarci și le printezi (quiz, flashcarduri, rezultate)."""

from html import escape as esc

from utile import formateaza_timp, sursa_text

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
    t = esc(str(valoare))
    if q is not None and q.get("tip") == "rw":
        t = t.replace("$", "\\$")
    return t


def html_pagina(titlu, corp, mathjax=False):
    extra = MATHJAX if mathjax else ""
    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="utf-8">
<title>{e(titlu)}</title>
<style>{CSS_PRINT}</style>
{extra}
</head>
<body>
<button class="nu-print" onclick="window.print()">Tipărește / Salvează ca PDF</button>
<h1>{e(titlu)}</h1>
{corp}
</body>
</html>"""


def html_quiz(quiz):
    litere = "ABCD"
    parti = ['<p class="mic">Nume: ______________ &nbsp; Data: ______________</p>']
    for i, q in enumerate(quiz, start=1):
        parti.append('<div class="intrebare">')
        parti.append(f"<p>{i}. {e(q['intrebare'])}</p>")
        for j, v in enumerate(q["variante"]):
            parti.append(f'<div class="varianta">&#9744; {litere[j]}. {e(v)}</div>')
        parti.append("</div>")

    parti.append('<div class="cheie"><h2>Răspunsuri corecte</h2>')
    for i, q in enumerate(quiz, start=1):
        corect = q["corect"]
        parti.append(
            f"<p>{i}. <b>{litere[corect]}. {e(q['variante'][corect])}</b> "
            f"<span class=\"mic\">({e(q.get('unitate', 'pagina'))} {e(q['pagina'])}) "
            f"{e(q['explicatie'])}</span></p>"
        )
    parti.append("</div>")
    return html_pagina("Quiz", "\n".join(parti))


def html_carduri(carduri):
    randuri = [
        "<table><tr><th>#</th><th>Întrebare</th><th>Răspuns</th><th>Sursa</th></tr>"
    ]
    for i, c in enumerate(carduri, start=1):
        randuri.append(
            f"<tr><td>{i}</td><td>{e(c['fata'])}</td>"
            f"<td>{e(c['spate'])}</td>"
            f"<td>{e(c.get('unitate', 'pagina'))} {e(c['pagina'])}</td></tr>"
        )
    randuri.append("</table>")
    return html_pagina("Flashcarduri", "\n".join(randuri))


def html_examen(titlu, scor, total, procent, folosit, de_recapitulat, detalii, mathjax):
    parti = [
        f"<p><b>Scor:</b> {scor}/{total} ({procent}%) &nbsp; "
        f"<b>Timp folosit:</b> {formateaza_timp(folosit)}</p>",
        "<h2>Ce să recapitulezi</h2>",
    ]
    if not de_recapitulat:
        parti.append("<p>Ai răspuns corect la toate întrebările.</p>")
    else:
        parti.append("<ul>")
        for eticheta, t, g in de_recapitulat:
            parti.append(f"<li><b>{e(eticheta)}</b>: {g} din {t} greșite</li>")
        parti.append("</ul>")

    parti.append("<h2>Întrebările</h2>")
    for i, q, ales, ok in detalii:
        clasa = "ok" if ok else "gresit"
        stare = "Corect" if ok else "Greșit"
        parti.append('<div class="intrebare">')
        if q.get("pasaj"):
            pasaj_html = e(q["pasaj"], q).replace("\n", "<br>")
            parti.append(f'<div class="pasaj">{pasaj_html}</div>')
        parti.append(
            f'<p class="{clasa}">{i + 1}. {e(q["intrebare"], q)} '
            f'<span class="mic">({stare})</span></p>'
        )
        parti.append(
            f"<div>Răspunsul tău: {e(ales, q) if ales else 'fără răspuns'}</div>"
        )
        if not ok:
            parti.append(
                f"<div>Răspuns corect: {e(q['variante'][q['corect']], q)}</div>"
            )
        explicatie = e(q["explicatie"], q).replace("\n", "<br>")
        parti.append(f'<div class="mic">{explicatie} ({e(sursa_text(q))})</div>')
        parti.append("</div>")
    return html_pagina(titlu, "\n".join(parti), mathjax=mathjax)
