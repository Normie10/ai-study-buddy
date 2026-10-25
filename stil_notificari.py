"""Stilul notificărilor fixe: mesajul „Se generează...” și avertismentul de
salvare plutesc pe ecran, oriunde ai fi dat scroll în pagină."""

CSS_NOTIFICARI = """
<style>
/* ---------- Notificare de încărcare (rotița din st.spinner) ----------
   Plutește sus, la mijloc, și rămâne vizibilă la scroll. */
[data-testid="stSpinner"] {
    position: fixed;
    top: 4rem;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: fit-content;
    max-width: calc(100vw - 2rem);
    z-index: 1000000;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.7rem 1.1rem;
    background: #16161A;
    border: 1px solid #3C3C45;
    border-left: 3px solid #E5383B;
    border-radius: 12px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.55);
    font-weight: 600;
    pointer-events: none;
}
/* Rotița lui Streamlit (primul element din notificare) o ascundem și o
   înlocuim cu un inel prop
