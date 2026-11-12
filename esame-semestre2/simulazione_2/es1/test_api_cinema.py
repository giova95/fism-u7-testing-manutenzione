"""ESERCIZIO 1: Black Box di un'API REST (35 punti). Testo completo: ../pratica.md.

Sostituite ogni LACUNA(n) con quello che va al suo posto.
"""

import pytest
import requests
from jsonschema import validate

from lacuna import LACUNA

BASE_URL = "http://localhost:8000"

# 1.1 (10 punti)
SCHEMA_FILM = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "durata": LACUNA(1),
        "in_sala": LACUNA(2),
    },
    "required": LACUNA(3),
    "additionalProperties": False,
}


def test_programmazione_rispetta_il_contratto():
    # Act
    risposta = requests.get(LACUNA(4), timeout=5)

    # Assert
    assert risposta.status_code == LACUNA(5)
    assert risposta.headers["Content-Type"] == LACUNA(6)
    film = risposta.json()
    assert LACUNA(7)                   # la lista non è vuota
    for un_film in film:
        LACUNA(8)                      # il film rispetta SCHEMA_FILM


# 1.2 (6 punti)
@pytest.mark.parametrize("film_id", LACUNA(9))
def test_film_inesistente_risponde_404_in_json(film_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/film/{film_id}", timeout=5)

    # Assert
    LACUNA(10)                         # lo status code
    LACUNA(11)                         # la chiave "errore" nel body


# 1.3 (6 punti)
def test_recensione_registrata():
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        LACUNA(12),                    # il body: voto 5 al film 1
        timeout=5,
    )

    # Assert
    assert risposta.status_code == LACUNA(13)
    assert LACUNA(14)                  # il body della risposta è quello del contratto


# 1.4 (13 punti)
@pytest.mark.parametrize("body_grezzo", [
    '{"film_id": 1, "voto": 5',        # JSON troncato (questo è già scritto)
    LACUNA(15),                        # body vuoto
    LACUNA(16),                        # manca il campo "voto"
    LACUNA(17),                        # il voto è del tipo sbagliato
])
def test_recensione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        LACUNA(18),                    # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    LACUNA(19)                         # una o due righe: status e chiave "errore"

# La domanda della lacuna (18), «perché qui non si può usare json=?», va in RISPOSTE.md.
