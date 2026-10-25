"""Mesajele de eroare pentru autentificare (perechi: română, engleză)."""

TEXTE_ERORI_AUTH = {
    "auth_err_credentiale": (
        "Email sau parolă greșite.",
        "Wrong email or password.",
    ),
    "auth_err_neconfirmat": (
        "Contul nu e confirmat încă. Deschide emailul primit la crearea "
        "contului și apasă pe linkul de confirmare (verifică și spam).",
        "Your account is not confirmed yet. Open the email you received when "
        "you created the account and click the confirmation link (check "
        "spam too).",
    ),
    "auth_err_existent": (
        "Există deja un cont cu acest email. Intră în cont din tab-ul "
        "alăturat sau folosește „Ai uitat parola?”.",
        "An account with this email already exists. Log in from the other "
        "tab or use “Forgot your password?”.",
    ),
    "auth_err_parola_slaba": (
        "Parola e prea slabă. Alege una mai lungă sau mai variată.",
        "The password is too weak. Choose a longer or more varied one.",
    ),
    "auth_err_parola_aceeasi": (
        "Parola nouă trebuie să fie diferită de cea veche.",
        "The new password must be different from the old one.",
    ),
    "auth_err_email_invalid": (
        "Adresa de email nu pare validă. Verific-o și încearcă din nou.",
        "The email address does not look valid. Check it and try again.",
    ),
    "auth_err_limita": (
        "Prea multe încercări într-un timp scurt. Așteaptă câteva minute "
        "și încearcă din nou.",
        "Too many attempts in a short time. Wait a few minutes and try "
        "again.",
    ),
    "auth_err_retea": (
        "Nu m-am putut conecta la server. Verifică conexiunea la internet "
        "și încearcă din nou.",
        "Could not reach the server. Check your internet connection and "
        "try again.",
    ),
    "auth_err_necunoscut": (
        "Ceva nu a mers. Încearcă din nou; dacă se repetă, trimite-mi "
        "detaliile de mai jos.",
        "Something went wrong. Try again; if it keeps happening, send me "
        "the details below.",
    ),
}
