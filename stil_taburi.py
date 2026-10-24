"""Stil pentru flashcarduri și pentru cronometrul plutitor de la examen."""

CSS_TABURI = """
<style>
/* ---------- Flashcard ---------- */
.fc {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    min-height: 12rem;
    padding: 1.75rem 1.5rem;
    margin: 0.25rem 0 0.75rem;
    text-align: center;
    border: 1px solid var(--border-hover);
    border-radius: 18px;
    background: linear-gradient(
        180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)
    );
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.35);
    animation: aparitie 0.35s ease both;
}
.fc-eticheta {
    color: var(--muted);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.fc-text {
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.35;
    letter-spacing: -0.01em;
}
.fc-raspuns {
    font-size: 1.1rem;
    font-weight: 500;
}
.fc-linie {
    width: 3rem;
    height: 3px;
    margin: 0.35rem 0;
    border-radius: 3px;
    background: var(--accent);
}
.fc-sursa {
    color: var(--muted);
    font-size: 0.8rem;
}
.fc-revine {
    padding: 0.15rem 0.65rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 700;
}

/* ---------- Cronometrul de la examen: plutește sus, în dreapta ---------- */
div[class*="st-key-cronometru_fix"] {
    position: fixed;
    top: 3.6rem;
    right: 1.25rem;
    z-index: 999990;
    width: fit-content;
    min-width: 9rem;
    padding: 0.5rem 0.9rem;
    background: #16161A;
    border: 1px solid #3C3C45;
    border-left: 3px solid #E5383B;
    border-radius: 12px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
}
div[class*="st-key-cronometru_fix"] [data-testid="stMetric"] {
    padding: 0;
    background: transparent;
    border: none;
}
@media (max-width: 640px) {
    div[class*="st-key-cronometru_fix"] {
        right: 0.5rem;
        min-width: 7.5rem;
    }
}
</style>
"""
