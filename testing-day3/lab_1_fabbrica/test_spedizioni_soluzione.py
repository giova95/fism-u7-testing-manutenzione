import pytest
from contextlib import nullcontext as does_not_raise
from spedizioni import calcola_spedizione

# 8 test cases, 1 sola funzione logica + nullcontext

@pytest.mark.parametrize("peso, zona, aspettativa, risultato_atteso", [
    # --- HAPPY PATHS ---
    # does_not_raise() è un context manager vuoto. Dice a Python: "Qui non deve succedere nulla".
    (1.5, "EU", does_not_raise(), 5.0),
    (3.0, "EU", does_not_raise(), 10.0),
    (1.5, "USA", does_not_raise(), 15.0),
    (5.0, "USA", does_not_raise(), 25.0),
    
    # --- SAD PATHS / EDGE CASES (Percorsi di Fallimento) ---
    # Sostituiamo il nullcontext con pytest.raises() e il risultato_atteso non importa (None).
    (-1.0, "EU", pytest.raises(ValueError, match="positivo"), None),
    (0.0,  "EU", pytest.raises(ValueError, match="positivo"), None),
    (2.0, "ASIA", pytest.raises(ValueError, match="supportata"), None),
    (2.0, "", pytest.raises(ValueError, match="supportata"), None)
])
def test_calcola_spedizione_universale(peso, zona, aspettativa, risultato_atteso):
    """
    Un SINGOLO test per ogni possibile combinazione.
    Il context manager 'aspettativa' deciderà se assorbire un errore o eseguire normalmente
    """
    with aspettativa:
        risultato = calcola_spedizione(peso, zona)
        # Questa riga viene eseguita solo se l'aspettativa era does_not_raise()
        # Se era pytest.raises(), l'eccezione interrompe il blocco 'with' e il test passa.
        assert risultato == risultato_atteso