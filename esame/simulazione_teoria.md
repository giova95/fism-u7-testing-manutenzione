# SIMULAZIONE DI ESAME #1: Parte Teorica (30 Minuti)

1. A cosa serve il comando git init?
   A) A copiare un repository da GitHub al PC.
   B) A creare il database nascosto .git per iniziare a tracciare i file in locale.
   C) A inviare il codice in produzione.

2. Qual è lo scopo della Staging Area in Git (raggiungibile con git add)?
   A) Eseguire i test automatici prima del commit
   B) Selezionare e preparare i file che faranno parte del prossimo commit
   C) Salvare i file in cloud come backup temporaneo

3. Qual è l'approccio standard dell'industria per sviluppare una nuova funzionalità senza rompere il codice in produzione?
   A) Lavorare su main ma fare commit solo a fine giornata.
   B) Creare una cartella separata sul PC e poi sovrascrivere i file.
   C) Staccare un nuovo branch (es. git checkout -b feature/login), sviluppare lì, e poi fare merge.

4. A cosa serve l'istruzione git push -u origin main?
   A) A scaricare gli ultimi aggiornamenti dal server.
   B) A cancellare il branch main sul server remoto.
   C) A caricare i commit locali sul server remoto (es. GitHub) e creare un collegamento permanente.

5. Qual è il comando da terminale per capire in quale cartella vi trovate fisicamente?
   A) ls o dir
   B) pwd o Get-Location
   C) cd ..

6. Perché si crea un Virtual Environment (python -m venv venv)?
   A) Per far girare il codice più velocemente.
   B) Per isolare le dipendenze del progetto (es. pytest) dal sistema operativo globale, evitando conflitti.
   C) Per nascondere il codice sorgente da occhi indiscreti.

7. Cosa contiene il file requirements.txt?
   A) Le password e i token del database.
   B) Il codice sorgente principale dell'applicazione.
   C) La lista esatta delle librerie di terze parti necessarie per far girare il progetto.

8. Come deve chiamarsi un file Python affinché pytest lo riconosca automaticamente come file di test?
   A) test\_\*.py o \_\*test.py
   B) verifica.py
   C) check\_\*.py

9. Se una funzione Python usa raise ValueError, cosa succede all'esecuzione del programma?
   A) Il programma stampa un avviso ma continua a girare.
   B) Il programma si interrompe immediatamente, impedendo la propagazione dell'errore.
   C) Il programma restituisce False.

10. Nello scrivere un test, a cosa serve il context manager pytest.raises?
    A) A far fallire volontariamente il test.
    B) A intercettare un'eccezione attesa, permettendo al test di passare (Happy path del Sad path).
    C) A sollevare i privilegi di amministratore.

# SIMULAZIONE DI ESAME #2: Parte Teorica (30 Minuti)

1. Perché i Senior misurano la "Branch Coverage" invece della semplice "Code Coverage"?
   A) Perché controlla che ogni diramazione logica (sia il True che il False di un if) sia stata effettivamente testata.
   B) Perché è l'unica metrica compatibile con GitHub.
   C) Perché analizza la copertura dei rami di Git.

2. A cosa serve il decoratore @pytest.mark.parametrize?
   A) A scaricare parametri da internet.
   B) A eseguire la stessa funzione di test decine di volte iniettando matrici di dati di input e output diversi, eliminando il codice duplicato.
   C) A generare numeri casuali per il test.

3. In una matrice parametrizzata, quando si usa contextlib.nullcontext?
   A) Quando ci si aspetta che la funzione sollevi un errore di rete.
   B) Quando i dati di input sono validi e la funzione deve terminare con successo senza sollevare eccezioni.
   C) Per cancellare le variabili in memoria dopo il test.

4. Se il file motore.py importa e usa random.randint, dove deve puntare la stringa del decoratore @patch?
   A) @patch('random.randint')
   B) @patch('test_motore.randint')
   C) @patch('motore.random.randint')

5. Qual è lo scopo primario di una pipeline di Continuous Integration (CI)?
   A) Ospitare il sito web per i clienti finali.
   B) Automatizzare l'esecuzione dei test su un server isolato a ogni push, bloccando il codice difettoso.
   C) Scrivere il codice al posto dei programmatori.

6. In quale directory esatta dovete inserire il file YAML affinché GitHub Actions lo riconosca?
   A) .github/workflows/
   B) actions/pipeline/
   C) src/.github/

7. Nello standard POSIX, a cosa è dedicato il canale stderr (Standard Error)?
   A) A raccogliere l'output principale del programma.
   B) A raccogliere log diagnostici, messaggi di errore o violazioni.
   C) A gestire l'input della tastiera.

8. Se uno script Python CLI termina con sys.exit(0), cosa capisce il sistema operativo?
   A) Che c'è stato un errore generico.
   B) Che il processo deve essere riavviato.
   C) Che il programma ha completato il suo compito con successo assoluto.

9. Perché nel Black Box Testing è vietato usare import mio_script nel file dei test?
   A) Perché viola l'isolamento: il Black Box deve interagire col programma solo tramite le interfacce di sistema (es. riga di comando), ignorandone il codice interno.
   B) Perché pytest non supporta l'istruzione import.
   C) Perché causa loop infiniti nella memoria RAM.

10. Quale libreria standard di Python si usa per testare le CLI tramite comandi di sistema (Black Box)?
    A) os.system
    B) subprocess
    C) sys.argv
