"""Simulazione 2, ESERCIZIO 2, Parte A (2A.2)."""

import requests


def test_biglietto_occupa_un_posto(base_url, auth):
    # Act
    risposta = requests.post(
        f"{base_url}/api/biglietti",
        json={"proiezione_id": 1},                                      # (26)
        headers=auth,                                                   # (27)
        timeout=5,
    )

    # Assert: non mi fido del 201, rileggo lo stato
    assert risposta.status_code == 201
    proiezione = requests.get(f"{base_url}/api/proiezioni/1", timeout=5).json()   # (28)
    assert proiezione["posti_liberi"] == 49                             # (29)
