"""Cuvintele care țin de limba CONTINUTULUI (a întrebărilor), nu de limba
interfeței. Cheia e valoarea internă a limbii întrebărilor (cea din pasul 1).
Pentru o limbă nouă, adaugă aici o intrare."""

CUVINTE_CONTINUT = {
    "română": {
        "adevarat": "Adevărat",
        "fals": "Fals",
        "prefix_af": "Adevărat sau fals: {intrebare}",
    },
    "engleză": {
        "adevarat": "True",
        "fals": "False",
        "prefix_af": "True or false: {intrebare}",
    },
}

LIMBA_IMPLICITA = "română"


def _cuvinte(q):
    limba = q.get("limba", LIMBA_IMPLICITA)
    return CUVINTE_CONTINUT.get(limba, CUVINTE_CONTINUT[LIMBA_IMPLICITA])


def varianta_ui(v, q):
    """Textul afișat pentru o variantă. La Adevărat/Fals, valorile interne
    rămân „Adevărat” și „Fals”; la afișare se traduc în limba întrebării."""
    if q.get("tip_intrebare") == "af":
        cuv = _cuvinte(q)
        if v == "Adevărat":
            return cuv["adevarat"]
        if v == "Fals":
            return cuv["fals"]
    return v


def text_intrebare_ui(q):
    """Textul întrebării, cu „Adevărat sau fals” (în limba întrebării) la
    afirmații."""
    if q.get("tip_intrebare") == "af":
        return _cuvinte(q)["prefix_af"].format(intrebare=q["intrebare"])
    return q["intrebare"]
