"""ESERCIZIO 2, Parte B (25 punti). NESSUN test deve contattare PagaSicuro."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from lacuna import LACUNA
from pagamenti import PagamentoNonDisponibile, addebita


# 2B.1 (7 punti)
@patch("lacuna.LACUNA_30")             # (30) sostituite la stringa. Regola del path: dove viene USATO
def test_addebito_restituisce_la_transazione(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = LACUNA(31)      # PagaSicuro risponde con la transazione "TX-42"
    mock_post.return_value = risposta_finta

    # Act
    codice = addebita(9.5)

    # Assert
    assert codice == "TX-42"
    _, kwargs = mock_post.call_args
    assert LACUNA(32)                  # timeout di al massimo 3 secondi


# 2B.2 (8 punti)
@pytest.mark.parametrize("guasto", LACUNA(33))         # PagaSicuro non risponde in tempo / è irraggiungibile
@patch("pagamenti.requests.post")
def test_guasto_diventa_errore_di_dominio(mock_post, guasto):
    # Arrange
    LACUNA(34)                         # il mock non risponde: ESPLODE con il guasto

    # Act + Assert
    with LACUNA(35):                   # ci aspettiamo l'eccezione di DOMINIO
        addebita(9.5)


# 2B.3 (5 punti)
@patch("pagamenti.requests.post")
def test_pagasicuro_risponde_503(mock_post):
    # Arrange: la chiamata RIESCE, è la risposta a contenere l'errore
    risposta_finta = MagicMock()
    risposta_finta.status_code = 503
    LACUNA(36)                         # raise_for_status() della risposta finta deve sollevare HTTPError
    LACUNA(37)                         # il mock restituisce la risposta finta

    # Act + Assert
    with pytest.raises(PagamentoNonDisponibile):
        addebita(9.5)
