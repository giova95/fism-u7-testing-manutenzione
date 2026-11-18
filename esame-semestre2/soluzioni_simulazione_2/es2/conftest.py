"""Simulazione 2, ESERCIZIO 2, Parte A (2A.1) — conftest con le lacune riempite."""

import os

import pytest
import requests


@pytest.fixture
def base_url():
    return os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(autouse=True)                                           # (20)
def stato_pulito(base_url):
    requests.post(f"{base_url}/api/reset", timeout=5)                   # (21)


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json={"email": "anna@aurora.it", "password": "Popcorn24"},      # (22)
        timeout=5,
    )
    return risposta.json()["token"]                                     # (23)


@pytest.fixture
def auth(token):                                                        # (24)
    return {"Authorization": f"Bearer {token}"}                         # (25)
