"""Simulazione 3, ESERCIZIO 2, Parte B — mock HTTP: SbloccoBici non viene mai contattato."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from sblocco import SbloccoNonDisponibile, sblocca


# 2B.1
@patch("sblocco.requests.post")                                         # (23) dove viene USATO
def test_lucchetto_aperto(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = {"sbloccata": True}              # (24)
    mock_post.return_value = risposta_finta

    # Act
    sbloccata = sblocca(2, "luca.verdi")

    # Assert
    assert sbloccata is True
    _, kwargs = mock_post.call_args
    assert kwargs["timeout"] <= 2                                       # (25)
    assert kwargs["json"]["stazione_id"] == 2                           # (26)


# 2B.2 (scritto per intero)
@pytest.mark.parametrize("guasto", [
    requests.Timeout("SbloccoBici non risponde in tempo"),
    requests.ConnectionError("SbloccoBici irraggiungibile"),
])
@patch("sblocco.requests.post")
def test_guasto_diventa_errore_di_dominio(mock_post, guasto):
    # Arrange: il mock non risponde, ESPLODE
    mock_post.side_effect = guasto

    # Act + Assert
    with pytest.raises(SbloccoNonDisponibile):
        sblocca(2, "luca.verdi")


# 2B.3 (scritto per intero)
@patch("sblocco.requests.post")
def test_sbloccobici_risponde_500(mock_post):
    # Arrange: la chiamata RIESCE, è la risposta a contenere l'errore
    risposta_finta = MagicMock()
    risposta_finta.status_code = 500
    risposta_finta.raise_for_status.side_effect = requests.HTTPError("500 Internal Server Error")
    mock_post.return_value = risposta_finta

    # Act + Assert
    with pytest.raises(SbloccoNonDisponibile):
        sblocca(2, "luca.verdi")
