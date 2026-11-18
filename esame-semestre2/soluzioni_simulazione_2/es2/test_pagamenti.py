"""Simulazione 2, ESERCIZIO 2, Parte B — mock HTTP: PagaSicuro non viene mai contattato."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from pagamenti import PagamentoNonDisponibile, addebita


# 2B.1
@patch("pagamenti.requests.post")                                       # (30) dove viene USATO
def test_addebito_restituisce_la_transazione(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = {"transazione": "TX-42"}         # (31)
    mock_post.return_value = risposta_finta

    # Act
    codice = addebita(9.5)

    # Assert
    assert codice == "TX-42"
    _, kwargs = mock_post.call_args
    assert kwargs["timeout"] <= 3                                       # (32)


# 2B.2
@pytest.mark.parametrize("guasto", [
    requests.Timeout("PagaSicuro non risponde in tempo"),               # (33)
    requests.ConnectionError("PagaSicuro irraggiungibile"),             # (33)
])
@patch("pagamenti.requests.post")
def test_guasto_diventa_errore_di_dominio(mock_post, guasto):
    # Arrange
    mock_post.side_effect = guasto                                      # (34)

    # Act + Assert
    with pytest.raises(PagamentoNonDisponibile):                        # (35)
        addebita(9.5)


# 2B.3
@patch("pagamenti.requests.post")
def test_pagasicuro_risponde_503(mock_post):
    # Arrange: la chiamata RIESCE, è la risposta a contenere l'errore
    risposta_finta = MagicMock()
    risposta_finta.status_code = 503
    risposta_finta.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")   # (36)
    mock_post.return_value = risposta_finta                             # (37)

    # Act + Assert
    with pytest.raises(PagamentoNonDisponibile):
        addebita(9.5)
