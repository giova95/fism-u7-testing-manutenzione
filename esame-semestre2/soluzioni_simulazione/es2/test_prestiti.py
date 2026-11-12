"""Simulazione, ESERCIZIO 2, Parte A (2A.2)."""

import requests


def test_prestito_rende_il_libro_non_disponibile(base_url, auth):
    # Act
    risposta = requests.post(f"{base_url}/api/prestiti", json={"libro_id": 1}, headers=auth, timeout=5)

    # Assert: non mi fido del 201, rileggo lo stato
    assert risposta.status_code == 201
    libro = requests.get(f"{base_url}/api/libri/1", timeout=5).json()
    assert libro["disponibile"] is False
