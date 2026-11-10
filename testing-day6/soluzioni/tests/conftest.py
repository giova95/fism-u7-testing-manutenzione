"""
conftest.py — il "magazzino" delle fixture.
pytest lo carica da solo: tutte le fixture definite qui sono disponibili
in ogni file di test della cartella, senza bisogno di import.
"""

import os

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def base_url():
    """Verifica UNA volta per sessione che il server sia acceso, poi restituisce l'URL."""
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=3)
    except requests.ConnectionError:
        pytest.exit(f"Il server {BASE_URL} è spento. Avvia 'python app.py' e riprova.")
    return BASE_URL


@pytest.fixture(autouse=True)
def stato_pulito(base_url):
    """Prima di OGNI test riporta il sistema allo stato iniziale (isolamento dei test)."""
    requests.post(f"{base_url}/api/reset", timeout=5)


@pytest.fixture
def token(base_url):
    """Fa il login come 'mario' e restituisce il token."""
    risposta = requests.post(
        f"{base_url}/api/login",
        json={"username": "mario", "password": "password123"},
        timeout=5,
    )
    assert risposta.status_code == 200, "Login fallito: la fixture non può procedere"
    return risposta.json()["token"]


@pytest.fixture
def auth(token):
    """Header di autenticazione pronto all'uso."""
    return {"Authorization": f"Bearer {token}"}
