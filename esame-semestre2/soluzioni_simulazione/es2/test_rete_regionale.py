"""Simulazione, ESERCIZIO 2, Parte B — mock HTTP: la rete regionale non viene mai contattata."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from rete_regionale import ReteNonDisponibile, copie_in_rete

ISBN = "9788845292613"


# 2B.1
@patch("rete_regionale.requests.get")                    # (23) dove viene USATO
def test_copie_lette_dalla_risposta(mock_get):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = {"copie": 3}       # (24)
    mock_get.return_value = risposta_finta

    # Act
    copie = copie_in_rete(ISBN)

    # Assert
    assert copie == 3
    _, kwargs = mock_get.call_args
    assert kwargs["timeout"] <= 2                         # (25)


# 2B.2
@pytest.mark.parametrize("guasto", [
    requests.Timeout("la rete non risponde in tempo"),
    requests.ConnectionError("la rete è irraggiungibile"),
])
@patch("rete_regionale.requests.get")
def test_guasto_di_rete_diventa_errore_di_dominio(mock_get, guasto):
    # Arrange: il mock non risponde, ESPLODE
    mock_get.side_effect = guasto

    # Act + Assert
    with pytest.raises(ReteNonDisponibile):
        copie_in_rete(ISBN)


# 2B.3
@patch("rete_regionale.requests.get")
def test_rete_risponde_500(mock_get):
    # Arrange: la chiamata RIESCE, è la risposta a contenere l'errore
    risposta_finta = MagicMock()
    risposta_finta.status_code = 500
    risposta_finta.raise_for_status.side_effect = requests.HTTPError("500 Internal Server Error")
    mock_get.return_value = risposta_finta

    # Act + Assert
    with pytest.raises(ReteNonDisponibile):
        copie_in_rete(ISBN)
