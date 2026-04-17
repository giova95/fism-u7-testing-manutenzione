# Homework: Il Quality Gate delle Password

## Contesto Aziendale

Il nostro sistema sta accettando password deboli. Dobbiamo implementare un modulo `validatore.py` che rispetti rigorose policy di sicurezza, supportato da una suite di test inespugnabile in `test_validatore.py`.

## Livello 1: Sopravvivenza (Obbligatorio per tutti)

1. Inizializza il virtual environment e installa `pytest`.
2. Scrivi la funzione `valida_password(password: str) -> bool`.
3. Scrivi i test per garantire che la funzione ritorni `True` solo se la password:
   - È lunga almeno 8 caratteri.
   - Contiene almeno un numero.
   - Contiene almeno una lettera maiuscola.

## Livello 2: Ingegneria (Standard)

1. Modifica la funzione: se la password è invalida, non deve ritornare `False`, ma deve "lanciare un'eccezione" personalizzata (es. `raise ValueError("Password troppo corta")`).
2. Aggiorna i test usando `pytest.raises` per intercettare l'eccezione esatta e verificare il messaggio d'errore.

## Livello 3: Escalation (Per chi vuole l'eccellenza)

Se hai finito i Livelli 1 e 2 in 20 minuti, il tuo codice probabilmente non scala.

1. **Parametrizzazione:** Usa `@pytest.mark.parametrize` per testare almeno 15 password invalide diverse con un singolo blocco di codice di test.
2. **Fixtures:** Crea un modulo che legge una lista di "password compromesse" da un file `blacklist.txt`. Scrivi una `pytest.fixture` che carichi questo file in memoria una sola volta prima di eseguire tutti i test, simulando un controllo contro un database reale.

---

## Istruzioni per la consegna
1. Dopo esservi assicurati che il programma funziona correttamente, scrivere il file requirements.txt con tutte le dipendenze necessarie a far funzionare il programma
2. Eliminare la cartella dove avete il virtual environment Python
3. Archiviare in .zip la cartella con il vostro programma, i test e il file dei requirements: potete usare winrar, winzip, 7zip, ... oppure direttamente dal terminale :)
4. Inviare lo zip alla mail angeligiovanni21@gmail.com
