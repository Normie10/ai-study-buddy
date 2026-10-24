"""Stil în plus pentru navigare și răspunsuri: taburile mici în formă de
pastilă, răspunsurile ca niște carduri și o aparițiune lină a conținutului."""

CSS_UI = """
<style>
/* ---------- Conținutul unui tab apare lin ---------- */
@keyframes aparitie_opac {
    from { opacity: 0; }
    to { opacity: 1; }
}
[data-baseweb="tab-panel"] {
    animation: aparitie_opac 0.3s ease both;
}

/* ---------- Taburile mari (Exersează, Învață, Progres) ---------- */
div[class*="st-key-nav_principal"] [data-testid="stTabs"] button[role="tab"] {
    font-size: 1.02rem;
    padding: 0.7rem 1.1rem;
}

/* ---------- Taburile mici (secțiunile): pastile ---------- */
div[class*="st-key-nav_sub"] [data-baseweb="tab-list"] {
    gap: 6px;
    width: fit-content;
    max-width: 100%;
    padding: 4px;
    margin-top: 0.4rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface);
}
div[class*="st-key-nav_sub"] button[role="tab"] {
    padding: 0.4rem 0.85rem;
    border-radius: 9px;
    font-size: 0.92rem;
}
div[class*="st-key-nav_sub"] button[role="tab"][aria-selected="true"] {
    background-color: var(--accent-soft);
    color: var(--accent);
}
div[class*="st-key-nav_sub"] [data-baseweb="tab-highlight"],
div[class*="st-key-nav_sub"] [data-baseweb="tab-border"] {
    display: none;
}

/* ---------- Variantele de răspuns, ca niște carduri ---------- */
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0.5rem;
}
[data-testid="stRadio"] div[role="radiogroup"] > label {
    margin: 0;
    padding: 0.6rem 0.9rem;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--surface);
    transition: border-color 0.15s ease, background-color 0.15s ease;
}
[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    border-color: var(--border-hover);
    background: rgba(255, 255, 255, 0.05);
}
[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    border-color: var(--accent);
    background: var(--accent-soft);
}
</style>
"""
