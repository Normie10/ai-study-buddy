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
/* Rotița originală a lui Streamlit se ascunde (orice copil fără text)... */
[data-testid="stSpinner"] > *:not(:has(p)):not(p) {
    display: none !important;
}
/* ...iar în locul ei desenăm una proprie, care se învârte. */
[data-testid="stSpinner"]::before {
    content: "";
    flex-shrink: 0;
    width: 18px;
    height: 18px;
    box-sizing: border-box;
    border: 2.5px solid rgba(255, 255, 255, 0.18);
    border-top-color: #E5383B;
    border-radius: 50%;
    animation: rotita-invartire 0.8s linear infinite;
}
@keyframes rotita-invartire {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ---------- Avertisment de salvare (bannerul galben) ----------
   Plutește jos, la mijloc, până apeși „Am înțeles”. */
div[class*="st-key-avert_salvare"] {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 1.25rem;
    margin: 0 auto;
    width: min(560px, calc(100vw - 2rem));
    max-height: 60vh;
    overflow-y: auto;
    z-index: 1000000;
}
/* Fundalul și bordura apar doar când există un avertisment în el */
div[class*="st-key-avert_salvare"]:has([data-testid="stAlert"]) {
    padding: 0.75rem;
    background: #16161A;
    border: 1px solid #3C3C45;
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
    animation: aparitie 0.25s ease both;
}
</style>
"""
