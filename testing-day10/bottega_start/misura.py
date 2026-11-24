"""
misura.py — fotografa lo STATO STAZIONARIO della Bottega (G5, Chaos Engineering).

Manda un po' di traffico realistico e risponde a due domande, endpoint per endpoint:
    1. quante richieste falliscono?        (tasso di errore: 5xx o nessuna risposta)
    2. quanto aspetta il cliente?          (latenza p50 e p95)

Uso (con app.py e corriere.py accesi):
    python misura.py                                  # 100 richieste al catalogo + 20 checkout
    python misura.py --checkout 100                   # più checkout = statistica più affidabile
    python misura.py --max-errori 1 --max-p95 1.0     # le soglie dell'ipotesi (default: 1% e 1 secondo)
    python misura.py --solo-lettura                   # niente checkout (es. contro la produzione)

Exit code (come le CLI del semestre 1):  0 = ipotesi verificata,  1 = ipotesi FALSIFICATA.

ATTENZIONE: il checkout chiama /api/reset (dati di prova!). Dopo averlo lanciato, nel browser
bisogna rifare il login.
"""

import argparse
import math
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TIMEOUT = 10                # nemmeno lo strumento di misura può aspettare per sempre
ORDINI_PRIMA_DEL_RESET = 40  # il cavo USB-C (id 4) ha stock 50: prima che finisca, rimettiamo a posto i dati


@dataclass
class Misura:
    endpoint: str
    status: int | None      # None = nessuna risposta (timeout, connessione rifiutata)
    secondi: float

    @property
    def fallita(self) -> bool:
        return self.status is None or self.status >= 500


def chiama(endpoint: str, metodo: str, percorso: str, **opzioni) -> Misura:
    inizio = time.perf_counter()
    try:
        risposta = requests.request(metodo, f"{BASE_URL}{percorso}", timeout=TIMEOUT, **opzioni)
        status = risposta.status_code
    except requests.RequestException:
        status = None
    return Misura(endpoint, status, time.perf_counter() - inizio)


def percentile(valori: list[float], p: float) -> float:
    """Percentile "nearest rank": il p95 è il valore sotto cui sta il 95% dei campioni."""
    ordinati = sorted(valori)
    posizione = math.ceil(p / 100 * len(ordinati)) - 1
    return ordinati[max(posizione, 0)]


# --- Il traffico ----------------------------------------------------------------

def traffico_catalogo(quante: int, thread: int) -> list[Misura]:
    """Tanti clienti che guardano il catalogo NELLO STESSO MOMENTO."""
    with ThreadPoolExecutor(max_workers=thread) as pool:
        return list(pool.map(lambda _: chiama("GET /api/prodotti", "GET", "/api/prodotti"), range(quante)))


def nuova_sessione() -> dict | None:
    """Riporta i dati allo stato iniziale e fa il login. None = siamo in produzione (reset vietato)."""
    if requests.post(f"{BASE_URL}/api/reset", timeout=TIMEOUT).status_code == 403:
        return None
    risposta = requests.post(
        f"{BASE_URL}/api/login", json={"username": "mario", "password": "password123"}, timeout=TIMEOUT
    )
    if risposta.status_code != 200:
        sys.exit(f"Login fallito ({risposta.status_code}): non posso misurare il checkout. Questo è già un sintomo!")
    return {"Authorization": f"Bearer {risposta.json()['token']}"}


def traffico_checkout(quanti: int) -> list[Misura]:
    """Un cliente che compra un cavo, `quanti` volte di fila (il carrello ha uno stato: niente parallelo)."""
    misure = []
    auth = None
    for i in range(quanti):
        if i % ORDINI_PRIMA_DEL_RESET == 0:
            auth = nuova_sessione()
            if auth is None:
                print("  (produzione: /api/reset vietato, salto il checkout)")
                return misure
        misure.append(chiama("POST /api/carrello", "POST", "/api/carrello",
                             json={"prodotto_id": 4, "quantita": 1}, headers=auth))
        misure.append(chiama("POST /api/ordini", "POST", "/api/ordini",
                             json={"cap": "50100"}, headers=auth))
    return misure


# --- Il rapporto ----------------------------------------------------------------

def rapporto(misure: list[Misura], max_errori: float, max_p95: float) -> bool:
    per_endpoint = defaultdict(list)
    for m in misure:
        per_endpoint[m.endpoint].append(m)

    print(f"\n{'endpoint':<20}{'richieste':>10}{'errori':>9}{'p50':>8}{'p95':>8}{'max':>8}   status")
    ipotesi_regge = True
    for endpoint, lista in per_endpoint.items():
        secondi = [m.secondi for m in lista]
        errori = 100 * sum(m.fallita for m in lista) / len(lista)
        p95 = percentile(secondi, 95)
        status = Counter("rete" if m.status is None else m.status for m in lista)
        regge = errori <= max_errori and p95 <= max_p95
        ipotesi_regge = ipotesi_regge and regge
        print(f"{endpoint:<20}{len(lista):>10}{errori:>8.1f}%{percentile(secondi, 50):>7.2f}s{p95:>7.2f}s"
              f"{max(secondi):>7.2f}s   {dict(sorted(status.items(), key=str))}  {'ok' if regge else '<-- FUORI SOGLIA'}")

    print(f"\nIpotesi: errori <= {max_errori}% e p95 <= {max_p95}s su ogni endpoint")
    print("VERDETTO: ipotesi VERIFICATA" if ipotesi_regge else "VERDETTO: ipotesi FALSIFICATA")
    return ipotesi_regge


def main() -> None:
    parser = argparse.ArgumentParser(description="Misura lo stato stazionario della Bottega")
    parser.add_argument("--catalogo", type=int, default=100, help="richieste al catalogo (default 100)")
    parser.add_argument("--thread", type=int, default=10, help="clienti in parallelo sul catalogo (default 10)")
    parser.add_argument("--checkout", type=int, default=20, help="checkout completi (default 20)")
    parser.add_argument("--max-errori", type=float, default=1.0, help="soglia errori in %% (default 1)")
    parser.add_argument("--max-p95", type=float, default=1.0, help="soglia p95 in secondi (default 1.0)")
    parser.add_argument("--solo-lettura", action="store_true", help="non fa checkout né reset")
    argomenti = parser.parse_args()

    try:
        requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
    except requests.RequestException:
        sys.exit(f"{BASE_URL} non risponde: la Bottega è accesa?")

    print(f"Misuro {BASE_URL} ...")
    inizio = time.perf_counter()
    misure = traffico_catalogo(argomenti.catalogo, argomenti.thread)
    if not argomenti.solo_lettura:
        misure += traffico_checkout(argomenti.checkout)
    print(f"Fatto in {time.perf_counter() - inizio:.1f}s")

    regge = rapporto(misure, argomenti.max_errori, argomenti.max_p95)
    sys.exit(0 if regge else 1)


if __name__ == "__main__":
    main()
