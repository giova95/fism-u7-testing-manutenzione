"""ESERCIZIO 2, Parte A, 2A.1 (12 punti): completate le lacune."""

import pytest
import requests

from lacuna import LACUNA


@pytest.fixture
def base_url():
    return "http://localhost:8000"


@pytest.fixture()                      # (20) tra le parentesi: deve girare prima di OGNI test, senza che nessun test la chieda
def stato_pulito(base_url):
    LACUNA(21)                         # riporta il server allo stato iniziale


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json=LACUNA(22),
        timeout=5,
    )
    return LACUNA(23)


@pytest.fixture
def auth(LACUNA_24):                   # (24) auth USA un'altra fixture: quale?
    return LACUNA(25)                  # l'header di autenticazione pronto all'uso
