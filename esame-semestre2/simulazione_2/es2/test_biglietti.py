"""ESERCIZIO 2, Parte A, 2A.2 (8 punti): completate le lacune."""

import requests

from lacuna import LACUNA


def test_biglietto_occupa_un_posto(base_url, auth):
    # Act
    risposta = requests.post(
        f"{base_url}/api/biglietti",
        json=LACUNA(26),               # un biglietto per la proiezione 1
        headers=LACUNA(27),
        timeout=5,
    )

    # Assert: non mi fido del 201, rileggo lo stato
    assert risposta.status_code == 201
    proiezione = requests.get(LACUNA(28), timeout=5).json()
    assert LACUNA(29)                  # all'inizio i posti liberi sono 50
