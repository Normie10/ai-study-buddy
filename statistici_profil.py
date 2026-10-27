"""Statistici rapide pentru meniul de profil: numărul real de încercări și
scorurile, fără limita de 50 de rânduri."""

from baza_date import _client, utilizator_curent


def statistici_progres():
    """Întoarce (rânduri, total_real). Rândurile conțin doar scor și total
    (cel mult 1000, cele mai noi); total_real e numărul exact de încercări
    din cont, cerut separat de la Supabase."""
    user = utilizator_curent()
    if user is None:
        return [], 0
    rezultat = (
        _client()
        .table("progres")
        .select("scor, total", count="exact")
        .eq("user_id", user.id)
        .order("creat_la", desc=True)
        .limit(1000)
        .execute()
    )
    randuri = rezultat.data or []
    total_real = rezultat.count if rezultat.count is not None else len(randuri)
    return randuri, total_real
