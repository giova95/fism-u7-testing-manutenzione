"""Simulazione, ESERCIZIO 2, Parte A (2A.1) — conftest con le lacune riempite."""

import os

import pytest
import requests


@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(autouse=True)                                                  # (17)
def stato_pulito(base_url):
    requests.post(f"{base_url}/api/reset", timeout=5)                          # (18)


@pytest.fixture
def token(base_url):
    risposta = requests.post(f"{base_url}/api/login",
                             json={"tessera": "T-1001", "pin": "4321"},        # (19)
                             timeout=5)
    return risposta.json()["token"]                                            # (20)


@pytest.fixture
def auth(token):                                                               # (21)
    return {"Authorization": f"Bearer {token}"}                                # (22)
