# rete_regionale.py — client della Rete Bibliotecaria Regionale (servizio esterno, NON è nostro)
import requests

RETE_URL = "https://rete.biblioteche.example/api"


class ReteNonDisponibile(Exception):
    """La rete regionale non risponde o risponde male: errore di DOMINIO, non di rete."""


def copie_in_rete(isbn: str) -> int:
    """Quante copie del libro si possono chiedere alle altre biblioteche della rete."""
    try:
        risposta = requests.get(f"{RETE_URL}/copie/{isbn}", timeout=2)
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise ReteNonDisponibile(str(errore)) from errore
    return risposta.json()["copie"]
