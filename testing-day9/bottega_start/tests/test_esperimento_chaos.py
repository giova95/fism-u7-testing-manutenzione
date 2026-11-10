"""
Test G1 (Lab 3) — Esperimento finale: cosa succede alla Bottega quando il fornitore esterno sta male?

Questo è un test BLACK BOX (passa da HTTP), ma richiede di "rompere" l'ambiente a mano:
    Esperimento A: spegnete corriere.py (CTRL+C)
    Esperimento B: riavviatelo lento ->  CORRIERE_LATENZA=10 python corriere.py
                   (Windows PowerShell: $env:CORRIERE_LATENZA=10; python corriere.py)
Si lancia SOLO esplicitamente:   pytest -m chaos
Ipotesi: la Bottega risponde 503 in meno di 4 secondi e il carrello NON viene perso.
"""

import pytest
import requests


@pytest.mark.chaos
def test_checkout_con_corriere_guasto_degrada_in_modo_controllato(base_url, auth):
    # Arrange
    requests.post(f"{base_url}/api/carrello", json={"prodotto_id": 4, "quantita": 1}, headers=auth, timeout=5)

    # Act — timeout lato test a 15s: se la Bottega si appende, il test lo deve DIMOSTRARE, non bloccarsi
    risposta = requests.post(f"{base_url}/api/ordini", json={"cap": "50100"}, headers=auth, timeout=15)

    # Assert
    assert risposta.status_code == 503
    assert risposta.json() == {"errore": "servizio spedizioni non disponibile"}
    assert risposta.elapsed.total_seconds() < 4
    carrello = requests.get(f"{base_url}/api/carrello", headers=auth, timeout=5).json()
    assert len(carrello["righe"]) == 1, "Il guasto del corriere ha fatto perdere il carrello al cliente!"
