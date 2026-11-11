# SIMULAZIONE DI ESAME: Parte Teorica (30 Minuti)

10 domande, una sola risposta corretta, 2 punti ciascuna. Le domande dell'esame vero saranno **diverse**, ma sugli stessi argomenti: soprattutto API, status code, stato pulito, fixture, mock ed eccezioni di dominio, l'esperimento sul corriere; poche domande di base su Playwright, codice legacy e pipeline.

1. Con il token di Giulia, un test chiama `GET /api/prenotazioni/42`, che appartiene a un altro socio. Quale status code vi aspettate da un'API scritta bene?
   A) `401 Unauthorized`, perché il token non vale per quella risorsa.
   B) `403 Forbidden` (oppure `404`, per non rivelare che la risorsa esiste): il server sa chi siete, ma non potete accedere a quella risorsa.
   C) `500 Internal Server Error`, perché la richiesta non è prevista.
   D) `200 OK`, perché il token è valido.

2. In un test con `@patch("spedizioni.requests.get")` volete verificare che il codice chiami il corriere con un timeout. Cosa usate?
   A) `mock_get.return_value`, che contiene il timeout impostato.
   B) `mock_get.side_effect = requests.Timeout()`: se il test passa, il timeout c'è.
   C) Niente: con un mock non si può verificare, serve un corriere lento vero.
   D) `mock_get.call_args`, che contiene gli argomenti con cui il mock è stato chiamato, e controllate la chiave `timeout`.

3. Volete verificare che il login risponda `400` a un JSON troncato, `'{"username": "mario"'`. Come lo spedite?
   A) Con `data='{"username": "mario"'` e l'header `Content-Type: application/json`: la stringa parte così com'è.
   B) Con `json='{"username": "mario"'`: `json=` serve proprio per spedire JSON.
   C) Con `json={"username": "mario"}`: è lo stesso JSON, solo scritto come dizionario.
   D) Non si può: `requests` rifiuta di spedire un JSON non valido.

4. Il contratto dice che un login fallito risponde **sempre** `"credenziali non valide"`, sia con un utente inesistente sia con una password sbagliata. Perché?
   A) Per risparmiare: un messaggio solo occupa meno memoria.
   B) Perché il server non è in grado di distinguere i due casi.
   C) Perché, se i messaggi fossero diversi, un attaccante potrebbe provare tanti nomi e scoprire quali utenti esistono; poi gli resterebbe da indovinare solo la password.
   D) Perché lo richiede il formato JSON.

5. Il corriere **risponde**, ma con lo status `503`. Come si simula nel mock, perché `spedizioni.py` sollevi `ServizioSpedizioniNonDisponibile`?
   A) Si costruisce una risposta finta con `raise_for_status.side_effect = requests.HTTPError("503")` e la si mette come `return_value` di `get`: la chiamata riesce, è la risposta a contenere l'errore.
   B) Si scrive `mock_get.side_effect = requests.ConnectionError()`: è la stessa cosa.
   C) Basta `risposta_finta.status_code = 503`: `raise_for_status()` di un `MagicMock` legge lo status da solo.
   D) Non si può simulare: bisogna spegnere il corriere vero.

6. Dopo la correzione del Lab 3, cosa risponde la Bottega a `POST /api/ordini` se il corriere non risponde entro 3 secondi?
   A) `500`, perché è un errore del server.
   B) `400`, perché il CAP potrebbe essere sbagliato.
   C) `201`, con una spedizione a costo zero.
   D) `503` con `{"errore": "servizio spedizioni non disponibile"}`, e il carrello resta intatto.

7. Prima di spegnere il corriere per l'esperimento, cosa si scrive?
   A) Niente: si spegne e si guarda cosa succede.
   B) L'**ipotesi**, con un risultato misurabile (per esempio «se il corriere è guasto, il checkout risponde 503 in meno di 4 secondi e il carrello resta pieno»): così il risultato dice qualcosa in ogni caso.
   C) La correzione del codice, così l'esperimento è già verde.
   D) Un `time.sleep(10)` nei test, per simulare il corriere lento.

8. Avete registrato il flusso d'acquisto con `codegen` e il codice generato gira verde. Cosa gli manca, quasi sempre, per essere un test?
   A) Niente: se gira verde, è un test.
   B) Un `time.sleep()` tra un'azione e l'altra, perché codegen va troppo veloce.
   C) Le asserzioni (`expect(...)`) su quello che l'utente deve vedere: senza, è una macro che clicca, non un test. Codegen serve a scoprire i locator.
   D) Un `print()` dopo ogni azione, così si vede nel terminale cosa ha fatto.

9. Arriva una segnalazione di bug su un codice legacy (come il ticket BOT-42 della demo). Scrivete il test che lo riproduce **prima** di correggere. Cosa deve succedere la prima volta che lo lanciate?
   A) Deve essere **rosso**, e rosso per il motivo giusto (il valore sbagliato, non un errore di import): dimostra che il test riproduce davvero il bug.
   B) Deve essere verde, altrimenti il test è scritto male.
   C) Non importa: conta solo che sia verde dopo la correzione.
   D) Non si lancia: un test che fallisce non va mai eseguito.

10. L'URL del deploy hook di Render permette a chiunque lo conosca di avviare un deploy. Come va usato nel workflow?
    A) Scritto in chiaro nel file YAML, tanto il repository è privato.
    B) Messo in un file `.env` committato nel repository.
    C) Passato come argomento da riga di comando a `pytest`.
    D) Salvato come **secret** del repository e letto con `${{ secrets.NOME }}`: non compare nel codice e GitHub lo maschera nei log.
