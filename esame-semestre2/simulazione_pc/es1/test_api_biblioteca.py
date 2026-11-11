"""ESERCIZIO 1: Black Box di un'API REST (35 punti). Testo completo: simulazione_pratica.md.

Sostituite ogni LACUNA(n) con quello che va al suo posto. Dove c'è scritto
«scrivete qui il test», scrivete la funzione intera.
"""

import pytest
import requests
from jsonschema import validate

from lacuna import LACUNA

BASE_URL = "http://localhost:8000"

# 1.1 (10 punti)
SCHEMA_LIBRO = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "autore": LACUNA(1),
        "disponibile": LACUNA(2),
    },
    "required": LACUNA(3),
    "additionalProperties": False,
}


def test_catalogo_rispetta_il_contratto():
    # Act
    risposta = requests.get(LACUNA(4), timeout=5)

    # Assert
    assert risposta.status_code == LACUNA(5)
    assert risposta.headers["Content-Type"] == LACUNA(6)
    libri = risposta.json()
    assert LACUNA(7)                   # la lista non è vuota
    for libro in libri:
        LACUNA(8)                      # il libro rispetta SCHEMA_LIBRO


# 1.2 (6 punti)
@pytest.mark.parametrize("libro_id", LACUNA(9))
def test_libro_inesistente_risponde_404_in_json(libro_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/libri/{libro_id}", timeout=5)

    # Assert
    LACUNA(10)                         # lo status code
    LACUNA(11)                         # la chiave "errore" nel body


# 1.3 (6 punti): scrivete qui il test del percorso felice di POST /api/suggerimenti con il titolo «Dune»



# 1.4 (13 punti)
@pytest.mark.parametrize("body_grezzo", [
    '{"titolo": "Dune"',               # JSON troncato (questo è già scritto)
    LACUNA(12),                        # body vuoto
    LACUNA(13),                        # JSON valido, ma è una lista e non un oggetto
    LACUNA(14),                        # titolo del tipo sbagliato
])
def test_suggerimento_non_valido_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/suggerimenti",
        LACUNA(15),                    # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    LACUNA(16)                         # una o due righe: status e chiave "errore"

# La domanda della lacuna (15), «perché qui non si può usare json=?», va in RISPOSTE.md.
