"""Simulazione 2, ESERCIZIO 1 — soluzione (black box). Lacune indicate con il numero, es. # (4)."""

import os

import pytest
import requests
from jsonschema import validate

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# 1.1
SCHEMA_FILM = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "durata": {"type": "integer"},                           # (1)
        "in_sala": {"type": "boolean"},                          # (2)
    },
    "required": ["id", "titolo", "durata", "in_sala"],           # (3)
    "additionalProperties": False,
}


def test_programmazione_rispetta_il_contratto():
    # Act
    risposta = requests.get(f"{BASE_URL}/api/film", timeout=5)          # (4)

    # Assert
    assert risposta.status_code == 200                                  # (5)
    assert risposta.headers["Content-Type"] == "application/json"       # (6)
    film = risposta.json()
    assert len(film) > 0                                                # (7)
    for un_film in film:
        validate(instance=un_film, schema=SCHEMA_FILM)                  # (8)


# 1.2
@pytest.mark.parametrize("film_id", ["999", "-1", "xyz"])              # (9)
def test_film_inesistente_risponde_404_in_json(film_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/film/{film_id}", timeout=5)

    # Assert
    assert risposta.status_code == 404                                  # (10)
    assert "errore" in risposta.json()                                  # (11)


# 1.3
def test_recensione_registrata():
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        json={"film_id": 1, "voto": 5},                                 # (12)
        timeout=5,
    )

    # Assert
    assert risposta.status_code == 201                                  # (13)
    assert risposta.json() == {"film_id": 1, "voto": 5}                 # (14)


# 1.4
@pytest.mark.parametrize("body_grezzo", [
    '{"film_id": 1, "voto": 5',            # JSON troncato
    "",                                    # (15) body vuoto
    '{"film_id": 1}',                      # (16) manca il voto
    '{"film_id": 1, "voto": "cinque"}',    # (17) voto del tipo sbagliato
])
def test_recensione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        data=body_grezzo,                                               # (18)
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    assert risposta.status_code == 400                                  # (19)
    assert "errore" in risposta.json()                                  # (19)
