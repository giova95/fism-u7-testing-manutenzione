"""
LAB 3 — Soluzione: isolare la dipendenza esterna (white box + mock).

Stesso @patch del semestre 1, ma ora il bersaglio è una chiamata HTTP.
Regola del path: intercetto 'requests.get' DOVE VIENE USATO -> 'spedizioni.requests.get'.
Questi test NON richiedono né app.py né corriere.py accesi.
"""

from unittest.mock import patch, MagicMock

import pytest
import requests

import spedizioni
from spedizioni import ServizioSpedizioniNonDisponibile


@pytest.fixture(autouse=True)
def stato_pulito():
    """Sovrascrive la fixture autouse del conftest: questi test non toccano il server."""
    yield


def risposta_finta(status: int, corpo: dict) -> MagicMock:
    finta = MagicMock()
    finta.status_code = status
    finta.json.return_value = corpo
    if status >= 400:
        finta.raise_for_status.side_effect = requests.HTTPError(f"{status}")
    return finta


# --- Livello 1: Sopravvivenza ------------------------------------------------

@patch("spedizioni.requests.get")
def test_costo_letto_dalla_risposta(mock_get):
    # Arrange
    mock_get.return_value = risposta_finta(200, {"costo": 4.9})

    # Act
    costo = spedizioni.costo_spedizione("50100", 1.5)

    # Assert
    assert costo == 4.9


@patch("spedizioni.requests.get")
def test_parametri_inviati_al_corriere(mock_get):
    mock_get.return_value = risposta_finta(200, {"costo": 4.9})

    spedizioni.costo_spedizione("50100", 1.5)

    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"cap": "50100", "peso": 1.5}


# --- Livello 2: Ingegneria — iniezione di guasti ----------------------------

@patch("spedizioni.requests.get")
def test_la_chiamata_ha_un_timeout(mock_get):
    """Senza timeout, se il corriere si blocca, si blocca anche la Bottega. Per sempre."""
    mock_get.return_value = risposta_finta(200, {"costo": 4.9})

    spedizioni.costo_spedizione("50100", 1.5)

    _, kwargs = mock_get.call_args
    assert "timeout" in kwargs
    assert kwargs["timeout"] <= 3


@pytest.mark.parametrize("guasto", [
    requests.Timeout("il corriere non risponde"),
    requests.ConnectionError("il corriere è spento"),
])
@patch("spedizioni.requests.get")
def test_guasto_di_rete_diventa_errore_di_dominio(mock_get, guasto):
    mock_get.side_effect = guasto

    with pytest.raises(ServizioSpedizioniNonDisponibile):
        spedizioni.costo_spedizione("50100", 1.5)


@patch("spedizioni.requests.get")
def test_corriere_risponde_503(mock_get):
    mock_get.return_value = risposta_finta(503, {"errore": "servizio temporaneamente non disponibile"})

    with pytest.raises(ServizioSpedizioniNonDisponibile):
        spedizioni.costo_spedizione("50100", 1.5)
