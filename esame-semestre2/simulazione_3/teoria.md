# SIMULAZIONE 3 (allenamento avanzato): Parte Teorica (30 minuti)

10 domande, una sola risposta corretta, 2 punti ciascuna. Le lettere vanno in `RISPOSTE.md`.

1. Il contratto dice che `POST /api/segnalazioni` con `stazione_id` del tipo sbagliato risponde `400`. Il vostro test manda `{"stazione_id": "uno", "testo": "freno rotto"}` e riceve `201`. Il test è rosso. Cosa significa?
   A) Il test è sbagliato: se il server accetta la segnalazione, va bene così.
   B) È un problema di rete: bisogna rilanciare il test.
   C) Il server è stato gentile: ha convertito "uno" in 1. Si cambia l'asserzione in `201`.
   D) È un difetto del server: non rispetta il contratto. Il test rosso è corretto e si segnala il bug.

2. Un secondo noleggio alla stazione 2, che non ha più bici, risponde `409`. Cosa vuol dire `409 Conflict`?
   A) Che il token non è valido.
   B) Che la richiesta è corretta, ma è in conflitto con lo **stato attuale** della risorsa: non ci sono più bici da noleggiare.
   C) Che il server è esploso.
   D) Che la stazione non esiste.

3. Nello schema di una stazione avete `properties` e `required` con i quattro campi, ma **non** `"additionalProperties": False`. Il server aggiunge un campo `"colore"`. Cosa succede al test?
   A) Resta verde: senza `additionalProperties: False` lo schema accetta i campi in più, e il contratto dice «esattamente».
   B) Diventa rosso: `required` vieta i campi non elencati.
   C) Va in errore: `jsonschema` non accetta campi sconosciuti.
   D) Diventa rosso solo se `"colore"` è un numero.

4. Perché il login sta in una fixture `token` nel `conftest.py`, invece di essere copiato in ogni test?
   A) Perché pytest non permette di chiamare `requests.post` dentro un test.
   B) Perché così il login si fa una volta sola per tutta la suite.
   C) Perché se l'endpoint di login cambia, si corregge **un punto solo**; e ogni test chiede `token` per nome, senza ripetere codice.
   D) Perché nel `conftest.py` le richieste sono più veloci.

5. Un test di `sblocca()` scrive `@patch("sblocco.sblocca")` e poi chiama `sblocca(2, "luca.verdi")`. È verde. Cosa verifica?
   A) Che `sblocca` gestisce bene il timeout.
   B) Niente: ha sostituito **la funzione stessa** che doveva testare con un mock. Il codice vero non gira mai (è un errore fatale).
   C) Che SbloccoBici risponde correttamente.
   D) Che il body inviato contiene la stazione giusta.

6. Nel test 2B.1 scrivete `_, kwargs = mock_post.call_args` e poi `assert kwargs["json"]["stazione_id"] == 2`. Cosa verificate?
   A) Che SbloccoBici ha risposto con la stazione 2.
   B) Che il server VeloCity ha salvato il noleggio.
   C) Che il mock restituisce un JSON valido.
   D) Che il nostro codice ha **spedito** a SbloccoBici il body giusto: `call_args` registra con quali argomenti è stato chiamato il mock.

7. Con SbloccoBici **spento**, il client riceve subito `ConnectionError`. Con SbloccoBici **lento** (10 secondi) e `timeout=2`, cosa riceve?
   A) `requests.Timeout` dopo circa 2 secondi: il timeout interrompe l'attesa.
   B) `ConnectionError` dopo 10 secondi.
   C) La risposta, dopo 10 secondi: il timeout vale solo per la connessione.
   D) Un `500` dal servizio.

8. Volete fare l'esperimento "SbloccoBici spento" sul sistema VeloCity. Cosa serve?
   A) Un test con `@patch` che simula SbloccoBici spento.
   B) Un `time.sleep(10)` nel test, per simulare il servizio lento.
   C) Un'ipotesi misurabile scritta **prima**, il sistema **acceso** con SbloccoBici spento davvero (in un ambiente di prova), e la misura di cosa riceve l'utente.
   D) Spegnere SbloccoBici in produzione e aspettare le segnalazioni dei clienti.

9. Il campo email ha `<label for="email">Email</label>` e `<input id="email">`. Quale locator usate nel test con il browser?
   A) `page.locator("#email")`
   B) `page.locator("form input").nth(0)`
   C) `page.locator("xpath=//div[2]/form/input[1]")`
   D) `page.get_by_label("Email")`

10. Il team vuole testare con Playwright tutti i 12 casi di errore di `POST /api/segnalazioni`. Cosa consigliate?
    A) Va bene: più test E2E ci sono, più il sistema è sicuro.
    B) Meglio i test delle **API** per i 12 casi d'errore: sono veloci e stabili. Con il browser si testa il flusso principale (la segnalazione inviata e il messaggio che vede l'utente).
    C) Nessun test: i casi d'errore li vede l'utente.
    D) Un solo test E2E con un `time.sleep` tra un caso e l'altro.
