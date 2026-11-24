"""
Client del servizio esterno del corriere (SpediVeloce S.p.A.).
Il servizio NON è nostro: non possiamo modificarlo, possiamo solo chiamarlo.
"""

import os

import requests

CORRIERE_URL = os.getenv("CORRIERE_URL", "http://localhost:8001")
TIMEOUT_SECONDI = 3


class ServizioSpedizioniNonDisponibile(Exception):
    """Il corriere non ha risposto, o ha risposto male. Errore di DOMINIO, non di rete."""


def costo_spedizione(cap: str, peso: float) -> float:
    try:
        risposta = requests.get(
            f"{CORRIERE_URL}/tariffa",
            params={"cap": cap, "peso": peso},
            timeout=TIMEOUT_SECONDI,
        )
        risposta.raise_for_status()
    except requests.RequestException as errore:
        # Traduco un problema di rete (dettaglio tecnico) in un problema di business
        raise ServizioSpedizioniNonDisponibile(str(errore)) from errore
    return risposta.json()["costo"]
