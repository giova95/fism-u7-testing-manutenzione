# test_gioco.py
import pytest
from unittest.mock import patch
from gioco import lancia_dado_magico

# IL SEGRETO PIÙ IMPORTANTE DEL MOCKING IN PYTHON:
# Non si mocka MAI dove l'oggetto è definito (es. 'random.randint')
# Si mocka DOVE l'oggetto viene usato (il nostro file 'gioco.py')
# Il path deve essere: "nome_file.libreria_importata.funzione"

@patch('gioco.random.randint')
def test_vittoria_garantita(mock_randint):
    # 1. SETUP: Trucco il dado. Dico al mock: "Quando ti chiamano, restituisci 6".
    mock_randint.return_value = 6
    
    # 2. EXECUTION: Eseguo la funzione. Lei crederà di usare il vero random!
    esito = lancia_dado_magico()
    
    # 3. ASSERTION
    assert esito == "Vittoria!"
    
    # ASSERTION AVANZATA: Verifico che la mia funzione mockata sia stata effettivamente chiamata
    mock_randint.assert_called_once_with(1, 6)

@patch('gioco.random.randint')
def test_sconfitta_garantita(mock_randint):
    # Trucco il dado per far uscire 1
    mock_randint.return_value = 1
    
    esito = lancia_dado_magico()
    assert esito == "Sconfitta!"