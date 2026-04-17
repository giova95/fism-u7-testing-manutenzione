from spedizioni import calcola_spedizione
import pytest

def test_spedizione_eu_leggera():
    assert calcola_spedizione(1.5, "EU") == 5.0

def test_spedizione_eu_pesante():
    assert calcola_spedizione(3.0, "EU") == 10.0

def test_spedizione_usa_leggera():
    assert calcola_spedizione(1.5, "USA") == 15.0

def test_spedizione_usa_pesante():
    assert calcola_spedizione(5.0, "USA") == 25.0

def test_peso_invalido():
    with pytest.raises(ValueError, match="positivo"):
        calcola_spedizione(-1.0, "EU")