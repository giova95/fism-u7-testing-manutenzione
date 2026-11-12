"""ESERCIZIO 1: Black Box di un'API REST (35 punti). Testo completo: ../pratica.md.

Sostituite ogni LACUNA(n) con quello che va al suo posto. Dove c'è scritto
«scrivete qui il test», scrivete la funzione intera.
"""

import pytest
import requests
from jsonschema import validate

from lacuna import LACUNA

BASE_URL = "http://localhost:8000"

# 1.1 (10 punti)
SCHEMA_STAZIONE = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "nome": {"type": "string"},
        "bici_libere": LACUNA(1),
        "attiva": LACUNA(2),
    },
    "required": LACUNA(3),
    "additionalProperties": False,
}


def test_stazioni_rispettano_il_contratto():
    # Act
    risposta = requests.get(LACUNA(4), timeout=5)

    # Assert
    assert risposta.status_code == LACUNA(5)
    assert risposta.headers["Content-Type"] == LACUNA(6)
    stazioni = risposta.json()
    assert LACUNA(7)                   # la lista non è vuota
    for stazione in stazioni:
        LACUNA(8)                      # la stazione rispetta SCHEMA_STAZIONE


# 1.2 (6 punti)
@pytest.mark.parametrize("stazione_id", LACUNA(9))
def test_stazione_inesistente_risponde_404_in_json(stazione_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/stazioni/{stazione_id}", timeout=5)

    # Assert
    LACUNA(10)                         # lo status code
    LACUNA(11)                         # la chiave "errore" nel body


# 1.3 (6 punti): scrivete qui il test del percorso felice di POST /api/segnalazioni
# (stazione 1, testo «freno rotto»)


# 1.4 (13 punti)
@pytest.mark.parametrize("body_grezzo", [
    '{"stazione_id": 1, "testo": "freno rotto"',     # JSON troncato (questo è già scritto)
    LACUNA(12),                        # manca il campo "testo"
    LACUNA(13),                        # stazione_id del tipo sbagliato
    LACUNA(14),                        # JSON valido, ma è una stringa e non un oggetto
])
def test_segnalazione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/segnalazioni",
        LACUNA(15),                    # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    LACUNA(16)                         # una o due righe: status e chiave "errore"

# La domanda della lacuna (14), «perché "freno rotto" tra virgolette è JSON valido ma va rifiutato?», va in RISPOSTE.md.
