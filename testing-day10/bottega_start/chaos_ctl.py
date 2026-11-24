"""
chaos_ctl.py — il telecomando del caos (G5). Funziona uguale su Mac e Windows.

    python chaos_ctl.py stato                                     # cosa è attivo adesso
    python chaos_ctl.py stop                                      # KILL SWITCH: spegne ogni guasto
    python chaos_ctl.py inietta --percorso /api/prodotti --latenza 2
    python chaos_ctl.py inietta --percorso /api/carrello --metodo POST --errori 0.5 --status 500
    python chaos_ctl.py inietta --percorso /api/ordini --kill
    python chaos_ctl.py orologio 2026-11-20                       # preventivo.py crede che oggi sia il 20/11
    python chaos_ctl.py orologio vero                             # torna all'orologio reale
    python chaos_ctl.py corriere --latenza 2.5 --errori 0.3       # avvia corriere.py "malato"

`inietta` AGGIUNGE una regola a quelle già attive. Per ripartire da zero: prima `stop`.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
URL_CHAOS = f"{BASE_URL}/api/chaos"
CARTELLA = Path(__file__).resolve().parent


def leggi_stato() -> dict:
    risposta = requests.get(URL_CHAOS, timeout=5)
    risposta.raise_for_status()
    return risposta.json()


def scrivi_stato(stato: dict) -> dict:
    risposta = requests.put(URL_CHAOS, json=stato, timeout=5)
    if risposta.status_code == 400:
        sys.exit(f"Configurazione rifiutata: {risposta.json()['errore']}")
    risposta.raise_for_status()
    return risposta.json()


def stampa(stato: dict) -> None:
    if not stato["regole"] and not stato["data_finta"]:
        print("Nessun guasto attivo.")
        return
    for regola in stato["regole"]:
        bersaglio = f"{regola['metodo'] or 'TUTTI'} {regola['percorso']}"
        if regola["kill"]:
            effetto = "KILL (502)"
        else:
            effetto = f"latenza {regola['latenza']}s, errori {regola['errori']:.0%} ({regola['status']})"
        print(f"  - {bersaglio}: {effetto}")
    if stato["data_finta"]:
        print(f"  - orologio di preventivo.py fermo al {stato['data_finta']}")


def comando_inietta(argomenti) -> None:
    regola = {
        "percorso": argomenti.percorso,
        "metodo": argomenti.metodo,
        "latenza": argomenti.latenza,
        "errori": argomenti.errori,
        "status": argomenti.status,
        "kill": argomenti.kill,
    }
    stato = leggi_stato()
    stato["regole"].append(regola)
    stampa(scrivi_stato(stato))


def comando_orologio(argomenti) -> None:
    stato = leggi_stato()
    stato["data_finta"] = None if argomenti.data == "vero" else argomenti.data
    stampa(scrivi_stato(stato))


def comando_stop(_argomenti) -> None:
    risposta = requests.delete(URL_CHAOS, timeout=5)
    risposta.raise_for_status()
    print("KILL SWITCH: tutti i guasti sono spenti.")


def comando_stato(_argomenti) -> None:
    stampa(leggi_stato())


def comando_corriere(argomenti) -> None:
    """Avvia corriere.py con le sue variabili d'ambiente, senza dover ricordare la sintassi di ogni shell."""
    ambiente = {
        **os.environ,
        "CORRIERE_LATENZA": str(argomenti.latenza),
        "CORRIERE_ERRORI": str(argomenti.errori),
    }
    try:
        subprocess.run([sys.executable, str(CARTELLA / "corriere.py")], env=ambiente, check=False)
    except KeyboardInterrupt:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Telecomando del chaos middleware della Bottega")
    sotto = parser.add_subparsers(dest="comando", required=True)

    sotto.add_parser("stato", help="mostra i guasti attivi").set_defaults(azione=comando_stato)
    sotto.add_parser("stop", help="KILL SWITCH: spegne tutti i guasti").set_defaults(azione=comando_stop)

    inietta = sotto.add_parser("inietta", help="aggiunge un guasto a un endpoint")
    inietta.add_argument("--percorso", required=True, help="es. /api/prodotti")
    inietta.add_argument("--metodo", choices=["GET", "POST", "PUT", "DELETE"], help="default: tutti")
    inietta.add_argument("--latenza", type=float, default=0.0, help="secondi di ritardo")
    inietta.add_argument("--errori", type=float, default=0.0, help="probabilità di errore, da 0 a 1")
    inietta.add_argument("--status", type=int, choices=[500, 503], default=503)
    inietta.add_argument("--kill", action="store_true", help="l'endpoint risponde 502 (processo morto)")
    inietta.set_defaults(azione=comando_inietta)

    orologio = sotto.add_parser("orologio", help="sposta la data vista da preventivo.py")
    orologio.add_argument("data", help="AAAA-MM-GG, oppure 'vero'")
    orologio.set_defaults(azione=comando_orologio)

    corriere = sotto.add_parser("corriere", help="avvia corriere.py con latenza/errori")
    corriere.add_argument("--latenza", type=float, default=0.0)
    corriere.add_argument("--errori", type=float, default=0.0)
    corriere.set_defaults(azione=comando_corriere)

    argomenti = parser.parse_args()
    try:
        argomenti.azione(argomenti)
    except requests.ConnectionError:
        sys.exit(f"La Bottega ({BASE_URL}) non risponde: è accesa?")
    except requests.HTTPError as errore:
        sys.exit(f"Errore dalla Bottega: {errore} (siete in produzione? il caos lì non esiste)")


if __name__ == "__main__":
    main()
