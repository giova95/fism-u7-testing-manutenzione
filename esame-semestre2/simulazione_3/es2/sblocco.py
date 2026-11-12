# sblocco.py — client di SbloccoBici (il servizio esterno che apre i lucchetti, NON è nostro)
import requests

SBLOCCO_URL = "https://api.sbloccobici.example"


class SbloccoNonDisponibile(Exception):
    """SbloccoBici non risponde o risponde male: errore di DOMINIO, non di rete."""


def sblocca(stazione_id: int, utente: str) -> bool:
    """Chiede a SbloccoBici di aprire il lucchetto di una bici della stazione. True se si è aperto."""
    try:
        risposta = requests.post(
            f"{SBLOCCO_URL}/sblocchi",
            json={"stazione_id": stazione_id, "utente": utente},
            timeout=2,
        )
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise SbloccoNonDisponibile(str(errore)) from errore
    return risposta.json()["sbloccata"]
