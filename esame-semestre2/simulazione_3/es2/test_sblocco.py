"""ESERCIZIO 2, Parte B (25 punti). NESSUN test deve contattare SbloccoBici."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from lacuna import LACUNA
from sblocco import SbloccoNonDisponibile, sblocca


# 2B.1 (7 punti)
@patch("lacuna.LACUNA_23")             # (23) sostituite la stringa. Regola del path: dove viene USATO
def test_lucchetto_aperto(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = LACUNA(24)
    mock_post.return_value = risposta_finta

    # Act
    sbloccata = sblocca(2, "luca.verdi")

    # Assert
    assert sbloccata is True
    _, kwargs = mock_post.call_args
    assert LACUNA(25)                  # timeout di al massimo 2 secondi
    assert LACUNA(26)                  # nel body inviato, la stazione è la 2


# 2B.2 (8 punti): scrivete qui UN'UNICA funzione di test parametrizzata:
# SbloccoBici che non risponde in tempo e SbloccoBici irraggiungibile -> SbloccoNonDisponibile


# 2B.3 (5 punti): scrivete qui il test di SbloccoBici che RISPONDE, ma con lo status 500 -> SbloccoNonDisponibile
