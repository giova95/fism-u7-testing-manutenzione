# Homework: Il Gateway di Pagamento

## Contesto

Il nostro gestionale ha un modulo per elaborare i pagamenti degli utenti. Questo modulo contiene rigide regole di business (validazione dei metodi, limiti per criptovalute, normative anti-riciclaggio) e fa una chiamata a un sistema bancario esterno per autorizzare la transazione.
Siccome il sistema esterno è imprevedibile, dobbiamo usare il Mocking per isolare i nostri test, e la parametrizzazione per evitare di scrivere decine di funzioni copia-incolla.

**Il Codice Sorgente:**
Trovate la logica di business da testare direttamente nel repository del corso, nel file: `testing-day3/homework/pagamenti.py`.
Leggetelo attentamente prima di scrivere i test. Prestate particolare attenzione a tutti gli `if` e all'operatore `and`.

## Livello 1: Sopravvivenza (Obbligatorio per tutti)

1. Inizializza il virtual environment e installa `pytest` e `pytest-cov`.
2. Crea il file `test_pagamenti.py`.
3. Scrivi tre test di base per verificare che le eccezioni funzionino correttamente (usa `pytest.raises`).
   - Un test che passi un importo negativo.
   - Un test che passi un metodo di pagamento non supportato (es. "contanti").
   - Un test che passi un importo superiore al saldo attuale.
     _(Nota: in questi casi il codice si ferma prima di chiamare la banca, quindi non serve ancora il mock)._

## Livello 2: Ingegneria (Standard)

Adesso dobbiamo testare i casi in cui i dati sono validi, ma se eseguiamo la funzione così com'è, il risultato sarà casuale (Flaky Test) per colpa della funzione esterna `autorizza_transazione`.

1. Usa il decoratore `@patch` per intercettare la funzione `autorizza_transazione` (ricordati la regola del path: intercetta dove viene usata!).
2. Scrivi un test in cui forzi la funzione mockata a restituire `True` e verifica che il pagamento di 50 euro con "carta" venga completato.
3. Scrivi un test in cui forzi la funzione mockata a restituire `False` e verifica che la transazione venga rifiutata.

## Livello 3: Escalation (Per chi vuole l'eccellenza)

Se hai finito i Livelli 1 e 2, il tuo codice funziona ma è verboso e probabilmente non copre tutti gli scenari. Ottimizziamolo.

1. **Parametrizzazione:** Usa `@pytest.mark.parametrize` per unire TUTTI i test del Livello 1 e i nuovi rami logici (come l'errore se si usa "crypto" con meno di 100 euro, o il messaggio anti-riciclaggio se si superano i 1000 euro).
2. **Il Pattern Universale:** Prova a unire _tutti_ i casi (sia quelli che danno errore, sia quelli che vanno a buon fine e usano il mock) in un'unica gigantesca funzione parametrizzata. Usa `contextlib.nullcontext` per gestire dinamicamente l'attesa di un errore (`pytest.raises`) o l'esecuzione pulita (`nullcontext`).
3. **Misura la verità:** Apri il terminale ed esegui il comando per misurare la Branch Coverage:
   `pytest --cov=pagamenti --cov-branch --cov-report=term-missing`
   Il tuo obiettivo è leggere `100%` di copertura senza NESSUNA riga segnalata nella colonna `Missing`. _Attenzione: l'operatore `and` richiede che testiate specifiche combinazioni per essere coperto interamente._

---

## Istruzioni per la consegna

1. Dopo esservi assicurati che il programma funzioni correttamente e che i test passino, scrivere il file `requirements.txt` con tutte le dipendenze necessarie.
2. **Eliminare la cartella dove avete il virtual environment Python.**
3. Archiviare in `.zip` la cartella con il vostro file dei test, il sorgente e i requirements. Potete usare winrar, winzip, 7zip, o il terminale.
4. Inviare lo zip alla mail `angeligiovanni21@gmail.com`
