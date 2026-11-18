"""Simulazione 3, ESERCIZIO 1 — soluzione (black box). Lacune indicate con il numero, es. # (4)."""

import os

import pytest
import requests
from jsonschema import validate

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# 1.1
SCHEMA_STAZIONE = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "nome": {"type": "string"},
        "bici_libere": {"type": "integer"},                      # (1)
        "attiva": {"type": "boolean"},                           # (2)
    },
    "required": ["id", "nome", "bici_libere", "attiva"],         # (3)
    "additionalProperties": False,
}


def test_stazioni_rispettano_il_contratto():
    # Act
    risposta = requests.get(f"{BASE_URL}/api/stazioni", timeout=5)      # (4)

    # Assert
    assert risposta.status_code == 200                                  # (5)
    assert risposta.headers["Content-Type"] == "application/json"       # (6)
    stazioni = risposta.json()
    assert len(stazioni) > 0                                            # (7)
    for stazione in stazioni:
        validate(instance=stazione, schema=SCHEMA_STAZIONE)             # (8)


# 1.2
@pytest.mark.parametrize("stazione_id", ["999", "0", "centrale"])      # (9)
def test_stazione_inesistente_risponde_404_in_json(stazione_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/stazioni/{stazione_id}", timeout=5)

    # Assert
    assert risposta.status_code == 404                                  # (10)
    assert "errore" in risposta.json()                                  # (11)


# 1.3 (scritto per intero)
def test_segnalazione_registrata():
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/segnalazioni",
        json={"stazione_id": 1, "testo": "freno rotto"},
        timeout=5,
    )

    # Assert
    assert risposta.status_code == 201
    corpo = risposta.json()
    assert corpo["stazione_id"] == 1
    assert corpo["testo"] == "freno rotto"
    assert isinstance(corpo["id"], int)


# 1.4
@pytest.mark.parametrize("body_grezzo", [
    '{"stazione_id": 1, "testo": "freno rotto"',          # JSON troncato
    '{"stazione_id": 1}',                                  # (12) manca il testo
    '{"stazione_id": "uno", "testo": "freno rotto"}',      # (13) stazione_id del tipo sbagliato
    '"freno rotto"',                                       # (14) JSON valido, ma è una stringa e non un oggetto
])
def test_segnalazione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/segnalazioni",
        data=body_grezzo,                                               # (15)
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    assert risposta.status_code == 400                                  # (16)
    assert "errore" in risposta.json()                                  # (16)
