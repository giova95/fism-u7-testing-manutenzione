"""Simulazione, ESERCIZIO 1 — soluzione di riferimento (black box). Lacune indicate con il numero, es. # (4)."""

import os

import pytest
import requests
from jsonschema import validate

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

SCHEMA_LIBRO = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "autore": {"type": "string"},                     # (1)
        "disponibile": {"type": "boolean"},               # (2)
    },
    "required": ["id", "titolo", "autore", "disponibile"],   # (3)
    "additionalProperties": False,
}


# 1.1
def test_catalogo_rispetta_il_contratto():
    risposta = requests.get(f"{BASE_URL}/api/libri", timeout=5)               # (4)
    assert risposta.status_code == 200                                        # (5)
    assert risposta.headers["Content-Type"] == "application/json"             # (6)
    libri = risposta.json()
    assert len(libri) > 0                                                     # (7)
    for libro in libri:
        validate(instance=libro, schema=SCHEMA_LIBRO)                         # (8)


# 1.2
@pytest.mark.parametrize("libro_id", ["999", "0", "abc"])                     # (9)
def test_libro_inesistente_risponde_404_in_json(libro_id):
    risposta = requests.get(f"{BASE_URL}/api/libri/{libro_id}", timeout=5)
    assert risposta.status_code == 404                                        # (10)
    assert "errore" in risposta.json()                                        # (11)


# 1.3
def test_suggerimento_registrato():
    risposta = requests.post(f"{BASE_URL}/api/suggerimenti", json={"titolo": "Dune"}, timeout=5)
    assert risposta.status_code == 201
    assert risposta.json()["titolo"] == "Dune"


# 1.4
@pytest.mark.parametrize("body_grezzo", [
    '{"titolo": "Dune"',        # JSON troncato
    "",                         # (12) body vuoto
    "[]",                       # (13) JSON valido ma non un oggetto
    '{"titolo": 42}',           # (14) tipo sbagliato
])
def test_suggerimento_non_valido_risponde_400(body_grezzo):
    risposta = requests.post(
        f"{BASE_URL}/api/suggerimenti",
        data=body_grezzo,                                                     # (15)
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    assert risposta.status_code == 400                                        # (16)
    assert "errore" in risposta.json()                                        # (16)
