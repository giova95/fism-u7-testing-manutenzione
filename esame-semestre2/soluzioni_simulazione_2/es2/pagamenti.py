# pagamenti.py — client di PagaSicuro (servizio esterno di pagamento, NON è nostro)
import requests

PAGASICURO_URL = "https://api.pagasicuro.example/v1"


class PagamentoNonDisponibile(Exception):
    """PagaSicuro non risponde o risponde male: errore di DOMINIO, non di rete."""


def addebita(importo: float) -> str:
    """Addebita l'importo del biglietto e restituisce il codice della transazione."""
    try:
        risposta = requests.post(f"{PAGASICURO_URL}/addebiti", json={"importo": importo}, timeout=3)
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise PagamentoNonDisponibile(str(errore)) from errore
    return risposta.json()["transazione"]
