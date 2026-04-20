import random

def lancia_dado_magico() -> str:
    """Se esce 6 vinci, altrimenti perdi."""
    risultato = random.randint(1, 6)
    
    if risultato == 6:
        return "Vittoria!"
    else:
        return "Sconfitta!"