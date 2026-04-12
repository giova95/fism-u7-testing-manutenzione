def applica_sconto(prezzo_base, codice_coupon):
    sconto_percentuale = 0
    sconto_fisso = 0

    if codice_coupon == "BENVENUTO5":
        sconto_fisso = 5
    elif codice_coupon == "SUMMER10":
        sconto_percentuale = 100 
        
    prezzo_scontato = prezzo_base - sconto_fisso
    prezzo_scontato = prezzo_scontato - (prezzo_scontato * sconto_percentuale / 100)
    
    return prezzo_scontato

def calcola_spedizione(prezzo_scontato, utente_premium):
    if utente_premium == True or prezzo_scontato > 50:
        return 0.0
    return 5.99

def elabora_batch_ordini(ordini):
    totale_giornata = 0
    print("--- INIZIO ELABORAZIONE BATCH ---")
    
    for ordine in ordini:
        cliente = ordine['cliente']
        
        prezzo_finale = applica_sconto(ordine['prezzo'], ordine['coupon'])
        spedizione = calcola_spedizione(prezzo_finale, ordine['premium'])
        
        totale_ordine = prezzo_finale + spedizione
        totale_giornata += totale_ordine
        
        print(f"✅ Ordine {cliente} elaborato: Totale da incassare {totale_ordine}€ (Di cui spedizione: {spedizione}€)")
        
    print(f"\n💰 TOTALE INCASSATO OGGI: {totale_giornata}€")

if __name__ == "__main__":
    ordini_di_oggi = [
        {"cliente": "Mario Rossi", "prezzo": 40.0, "coupon": None, "premium": False},
        {"cliente": "Luigi Verdi", "prezzo": 50.0, "coupon": None, "premium": False},      
        {"cliente": "Anna Neri", "prezzo": 3.0, "coupon": "BENVENUTO5", "premium": True},  
        {"cliente": "Giulia Bianchi", "prezzo": 250.0, "coupon": "SUMMER10", "premium": False} 
    ]
    
    elabora_batch_ordini(ordini_di_oggi)