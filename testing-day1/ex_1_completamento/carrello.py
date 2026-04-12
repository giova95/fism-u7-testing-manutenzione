def calcola_iva(prezzo_netto, aliquota_iva=22):
    """
    Calcola l'importo dell'IVA su un prezzo netto.
    Esempio: su 100 euro con aliquota 22, l'IVA è 22.
    """
    # TODO: Implementa la logica qui
    pass

def applica_sconto(prezzo, percentuale_sconto):
    """
    Applica uno sconto percentuale a un prezzo.
    Ritorna il nuovo prezzo scontato.
    """
    # TODO: Implementa la logica qui
    pass

def calcola_totale_carrello(lista_prezzi_netti, percentuale_sconto=0):
    """
    1. Somma tutti i prezzi netti.
    2. Calcola e aggiunge l'IVA al 22% sul totale netto.
    3. Applica lo sconto percentuale sul totale lordo (netto + IVA).
    Ritorna il totale finale da pagare.
    """
    # TODO: Implementa la logica unendo le funzioni precedenti
    pass

# --- ZONA DI TEST MANUALE (Non toccare) ---
if __name__ == "__main__":
    print("--- INIZIO ELABORAZIONE CARRELLO ---")
    articoli = [100.0, 50.0, 200.0]
    
    try:
        totale_da_pagare = calcola_totale_carrello(articoli, percentuale_sconto=10)
        print(f"Totale Netto inserito: {sum(articoli)} EUR")
        print(f"Totale Finale (con IVA 22% e Sconto 10%): {totale_da_pagare} EUR")
        print("Se il risultato è 384.3, hai fatto un ottimo lavoro.")
    except Exception as e:
        print(f"ERRORE GRAVE: Il tuo codice è andato in crash. Dettaglio: {e}")