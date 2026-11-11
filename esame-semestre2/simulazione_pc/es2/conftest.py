"""ESERCIZIO 2, Parte A, 2A.1 (13 punti): completate le lacune."""

import pytest
import requests

from lacuna import LACUNA


@pytest.fixture
def base_url():
    return "http://localhost:8000"


@pytest.fixture()                      # (17) tra le parentesi: deve girare prima di OGNI test, senza che nessun test la chieda
def stato_pulito(base_url):
    LACUNA(18)                         # riporta il server allo stato iniziale


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json=LACUNA(19),
        timeout=5,
    )
    return LACUNA(20)


@pytest.fixture
def auth(LACUNA_21):                   # (21) auth USA un'altra fixture: quale?
    return LACUNA(22)                  # l'header di autenticazione pronto all'uso
