"""Simulazione 3, ESERCIZIO 2, Parte A (2A.2) — scritto per intero."""

import requests


def test_ultima_bici_noleggiata_poi_409(base_url, auth):
    # Act: noleggio l'unica bici della stazione 2
    risposta = requests.post(f"{base_url}/api/noleggi", json={"stazione_id": 2}, headers=auth, timeout=5)

    # Assert: non mi fido del 201, rileggo la stazione
    assert risposta.status_code == 201
    stazione = requests.get(f"{base_url}/api/stazioni/2", timeout=5).json()
    assert stazione["bici_libere"] == 0

    # Un secondo noleggio alla stessa stazione: non ci sono più bici
    di_nuovo = requests.post(f"{base_url}/api/noleggi", json={"stazione_id": 2}, headers=auth, timeout=5)
    assert di_nuovo.status_code == 409
    assert "errore" in di_nuovo.json()
