import random

def autorizza_transazione(importo: float) -> bool:
    """Simula una chiamata a un sistema bancario esterno. È imprevedibile!"""
    return random.choice([True, False])

def elabora_pagamento(metodo: str, saldo_attuale: float, importo: float) -> str:
    """Logica principale del sistema di pagamento."""
    if importo <= 0:
        raise ValueError("L'importo deve essere maggiore di zero.")
        
    metodi_validi = ["carta", "paypal", "crypto"]
    if metodo not in metodi_validi:
        raise ValueError("Metodo di pagamento non supportato.")
        
    if metodo == "crypto" and importo < 100:
        raise ValueError("L'importo minimo per le crypto è 100.")
        
    if saldo_attuale < importo:
        raise ValueError("Fondi insufficienti per completare la transazione.")
        
    if not autorizza_transazione(importo):
        return "Transazione rifiutata dalla banca."
        
    if importo > 1000:
        return "Pagamento completato. Richiesta verifica anti-riciclaggio."
        
    return "Pagamento completato con successo."