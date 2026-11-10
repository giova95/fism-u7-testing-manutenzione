"""
Il primo test di sistema: il server è vivo?
Prerequisito: python app.py acceso in un altro terminale.
(L'URL arriva dalla fixture base_url di conftest.py: si cambia con la variabile BASE_URL.)
"""

import requests


def test_health_risponde_ok(base_url):
    # Act
    risposta = requests.get(f"{base_url}/api/health", timeout=5)

    # Assert
    assert risposta.status_code == 200
    assert risposta.json()["status"] == "ok"
