import pytest
import datetime
from unittest.mock import patch
from licenze import licenza_scaduta

# =====================================================================
# SOLUZIONE: Il Mocking del Tempo
# =====================================================================

# REGOLA D'ORO DEL PATHING: 
# Non scriviamo @patch('datetime.datetime.now') perché il modulo nativo è in C
# "Mockiamo" il namespace 'datetime' ESATTAMENTE come è stato importato dentro 'licenze.py'.
@patch('licenze.datetime')
def test_licenza_scaduta_nel_passato(mock_datetime):
    
    # 1. SETUP: La macchina del tempo. Creiamo un "oggi" finto
    # Fissiamo il tempo al 1 Gennaio 2024
    finto_oggi = datetime.datetime(2024, 1, 1)
    
    # Diciamo alla nostra funzione "mockata" di restituire la data finta quando qualcuno chiama now()
    mock_datetime.datetime.now.return_value = finto_oggi
    
    # IL FIX ARCHITETTURALE (Side Effect):
    # Attenzione! Avendo mockato interamente 'datetime', il codice in licenze.py
    # non saprà più come usare 'strptime' per convertire la stringa in data e crasherà.
    # Usiamo 'side_effect' per dire al mock: "Quando ti chiedono strptime, usa la funzione vera di Python".
    mock_datetime.datetime.strptime.side_effect = datetime.datetime.strptime
    
    # 2. EXECUTION & 3. ASSERTION
    # Rispetto al nostro finto "oggi" (2024), una licenza del 2023 DEVE risultare scaduta (True).
    assert licenza_scaduta("2023-12-31") is True

@patch('licenze.datetime')
def test_licenza_ancora_valida(mock_datetime):
    # Setup identico per fermare il tempo
    mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)
    mock_datetime.datetime.strptime.side_effect = datetime.datetime.strptime
    
    # Rispetto al nostro finto "oggi" (2024), una licenza del 2025 NON è scaduta (False).
    assert licenza_scaduta("2025-06-15") is False