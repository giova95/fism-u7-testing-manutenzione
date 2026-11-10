"""
Golden master di preventivo.calcola_totale — STARTER (quasi pronto).

Copiatelo nella cartella tests_preventivo/ del vostro repository, insieme a conftest.py e
test_preventivo_golden_master.py (stessa cartella starter/).
Non è un file di test (non inizia con test_): è il "banco di prova" usato dal test.
Per provarlo da solo, dalla radice del repository (dove c'è preventivo.py):

    python -m tests_preventivo.golden_master

C'è UN solo TODO da completare: la lista DATE.
"""

import contextlib
import datetime
import io
import itertools
import json
from pathlib import Path
from unittest.mock import patch

import preventivo

FILE_APPROVATO = Path(__file__).parent / "approvato_preventivo.json"

# --- Le "manopole". Ogni valore è scelto per un MOTIVO (vedi i commenti) ---

CARRELLI = {
    "vuoto": [],
    "cavo": [{"prezzo": 9.99, "quantita": 1}],                 # meno di 10 €: BENVENUTO10 va sotto zero
    "mouse": [{"prezzo": 34.5, "quantita": 1}],
    "sotto_soglia": [{"prezzo": 49.99, "quantita": 1}],        # soglia della spedizione gratuita
    "sopra_soglia": [{"prezzo": 50.0, "quantita": 1}],
    "benvenuto_al_limite": [{"prezzo": 59.99, "quantita": 1}],  # 59,99 - 10 = 49,99: di nuovo sotto soglia
    "tastiera": [{"prezzo": 89.9, "quantita": 1}],
    "vip_100": [{"prezzo": 100.0, "quantita": 1}],             # soglia dello sconto VIP (> 100)
    "vip_100_01": [{"prezzo": 100.01, "quantita": 1}],
    "vip_101_10": [{"prezzo": 101.1, "quantita": 1}],
    "misto": [
        {"prezzo": 89.9, "quantita": 1},
        {"prezzo": 34.5, "quantita": 2},
        {"prezzo": 9.99, "quantita": 3},
    ],
    "righe_sporche": [                                         # righe che il legacy scarta in silenzio
        {"prezzo": 34.5, "quantita": 0},
        {"prezzo": 34.5, "quantita": -3},
        {"prezzo": -5.0, "quantita": 2},
        {"prezzo": 0.5, "quantita": 2},
        {"prezzo": 9.99, "quantita": 2},
    ],
}
TIPI_CLIENTE = ["nuovo", "vip", "altro"]                   # "altro": né nuovo né VIP
CODICI = ["", "BENVENUTO10", "BLACKFRIDAY", "benvenuto10"]  # "benvenuto10": scritto male (minuscolo)
CAP = ["50100", "07100", "08100", "09100", "90100", "98100", "99100"]  # Firenze, Sardegna x3, Sicilia x2, fuori range
SPEDIZIONI = [4.9]                                         # tariffa standard di SpediVeloce

# TODO: i BORDI della finestra del Black Friday. Guardate in preventivo.py quali giorni la delimitano
# e mettete: il giorno PRIMA della finestra, il PRIMO giorno, l'ULTIMO giorno,
# e un giorno con il numero "giusto" ma nel mese sbagliato. Al posto di "2026-11-10".
DATE = ["2026-11-10"]


def genera_casi():
    """Prodotto cartesiano di tutte le manopole: ogni combinazione è un caso."""
    for carrello, tipo, codice, cap, sped, oggi in itertools.product(
        CARRELLI, TIPI_CLIENTE, CODICI, CAP, SPEDIZIONI, DATE
    ):
        yield {"carrello": carrello, "tipo": tipo, "codice": codice, "cap": cap, "sped": sped, "oggi": oggi}


def esegui_caso(caso):
    """Esegue UN caso in condizioni controllate e restituisce il totale."""
    # Nemico 1, lo STATO GLOBALE: senza questa riga BENVENUTO10 varrebbe solo per il PRIMO caso
    preventivo.SCONTI_USATI.clear()

    # Nemico 2, il TEMPO: fermo l'orologio DOVE VIENE USATO (preventivo.datetime), regola del path
    with patch("preventivo.datetime") as finto_datetime:
        finto_datetime.date.today.return_value = datetime.date.fromisoformat(caso["oggi"])

        # Nemico 3, i PRINT di debug: decidiamo NOI che non fanno parte del comportamento, e li zittiamo
        with contextlib.redirect_stdout(io.StringIO()):
            return preventivo.calcola_totale(
                CARRELLI[caso["carrello"]], caso["tipo"], caso["codice"], caso["cap"], caso["sped"]
            )


def fotografa():
    """Esegue tutti i casi e restituisce la lista {input..., totale}."""
    return [{**caso, "totale": esegui_caso(caso)} for caso in genera_casi()]


def salva(risultati, percorso=FILE_APPROVATO):
    # Un caso per riga: così "git diff" mostra ESATTAMENTE quali casi sono cambiati
    righe = ",\n".join(json.dumps(r, ensure_ascii=False) for r in risultati)
    percorso.write_text(f"[\n{righe}\n]\n", encoding="utf-8")


def carica(percorso=FILE_APPROVATO):
    return json.loads(percorso.read_text(encoding="utf-8"))


if __name__ == "__main__":
    risultati = fotografa()
    print(f"{len(risultati)} casi. I primi 5:")
    for r in risultati[:5]:
        print(r)
