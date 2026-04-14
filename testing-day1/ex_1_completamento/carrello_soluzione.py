def calcola_iva(prezzo_netto, aliquota_iva=22):
    """
    Calcola l'importo dell'IVA su un prezzo netto.
    """
    # SPIEGAZIONE: Divido l'aliquota per 100 per calcolare iva
    return prezzo_netto * (aliquota_iva / 100)

def applica_sconto(prezzo, percentuale_sconto):
    """
    Applica uno sconto percentuale a un prezzo.
    Ritorna il nuovo prezzo scontato.
    """
    # SPIEGAZIONE: Sottraggo dal prezzo originario la quota percentuale calcolata
    sconto = prezzo * (percentuale_sconto / 100)
    return prezzo - sconto

def calcola_totale_carrello(lista_prezzi_netti, percentuale_sconto=0):
    """
    Logica di orchestrazione del carrello.
    """
    # 1. Somma di tutti i prezzi netti (Uso la funzione di base python 'sum')
    totale_netto = sum(lista_prezzi_netti)
    
    # 2. Calcolo l'IVA sfruttando la funzione dedicata
    totale_iva = calcola_iva(totale_netto)
    totale_lordo = totale_netto + totale_iva
    
    # 3. Applico lo sconto sul totale lordo
    totale_finale = applica_sconto(totale_lordo, percentuale_sconto)
    
    return totale_finale

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