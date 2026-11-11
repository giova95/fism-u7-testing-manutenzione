"""ESERCIZIO 2, Parte B (25 punti). NESSUN test deve contattare la rete regionale."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from lacuna import LACUNA
from rete_regionale import ReteNonDisponibile, copie_in_rete


# 2B.1 (7 punti)
@patch("lacuna.LACUNA_23")             # (23) sostituite la stringa. Regola del path: dove viene USATO
def test_copie_lette_dalla_risposta(mock_get):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = LACUNA(24)
    mock_get.return_value = risposta_finta

    # Act
    copie = copie_in_rete("9788845292613")

    # Assert
    assert copie == 3
    _, kwargs = mock_get.call_args
    assert LACUNA(25)                  # timeout di al massimo 2 secondi


# 2B.2 (8 punti): scrivete qui UN'UNICA funzione di test parametrizzata:
# rete che non risponde in tempo e rete irraggiungibile -> ReteNonDisponibile



# 2B.3 (5 punti): scrivete qui il test della rete che RISPONDE, ma con lo status 500 -> ReteNonDisponibile

