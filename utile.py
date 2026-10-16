"""Funcții mici, folosite în mai multe locuri."""


def fmt(n):
    """Număr cu puncte ca separator de mii: 150000 -> 150.000"""
    return f"{n:,}".replace(",", ".")


def norm(text):
    """Text normalizat (litere mici, spații curate), pentru comparații."""
    return " ".join(str(text).lower().split())


def formateaza_timp(secunde):
    secunde = max(int(secunde), 0)
    return f"{secunde // 60:02d}:{secunde % 60:02d}"


def text_din_unitati(unitati, eticheta):
    """Textul trimis modelului, cu o etichetă [Pagina N] înaintea fiecărei bucăți."""
    nume = eticheta.capitalize()
    return "\n\n".join(f"[{nume} {u['pagina']}]\n{u['text']}" for u in unitati)


def md(text, q):
    """Pregătește textul pentru Markdown. La Reading and Writing, semnul $ nu
    trebuie interpretat ca formulă. Reface și rândurile noi."""
    text = str(text)
    if q.get("tip") == "rw":
        text = text.replace("$", "\\$")
    return text.replace("\n", "  \n")


def sursa_text(q):
    """De unde provine o întrebare: tema (SAT) sau pagina/secțiunea (document)."""
    if q.get("tema"):
        return q["tema"]
    return f"{q.get('unitate', 'pagina')} {q.get('pagina', '?')}"


def eticheta_grup(q):
    """Eticheta după care se grupează greșelile în raportul de la examen."""
    if q.get("tema"):
        return q["tema"]
    u = q.get("unitate", "pagina").capitalize()
    p = str(q.get("pagina", "?"))
    return f"{u} necunoscută" if p == "?" else f"{u} {p}"
