# RECAP GIORNO 5: Continuous Integration e Black Box Testing

L'obiettivo di oggi era distruggere definitivamente la frase peggiore che un programmatore possa pronunciare: "Sul mio PC funziona". Abbiamo abbandonato l'ambiente inquinato del vostro computer locale per abbracciare l'automazione in cloud. Successivamente, abbiamo smesso di guardare il codice col microscopio e abbiamo iniziato a testarlo come farebbe un sistema operativo. Di seguito i pattern architetturali e i contratti di sistema che abbiamo stabilito.

---

## 1. Continuous Integration (Il Quality Gate)

Come detto da inizio modulo il vostro PC è un ambiente sporco, pieno di dipendenze globali installate per caso. Uno sviluppatore esperto non si fida del proprio PC ma si fida di un ambiente sterile, governato dall'Infrastructure as Code

Ogni volta che fate un push, una pipeline di CI (Continuous Integration) prende in affitto un server immacolato, scarica il codice, installa le dipendenze ed esegue i test

- Pallino Verde: Il codice è valido e rispetta le regole di business

- Pallino Rosso: Il vostro codice è respinto. Il progetto è bloccato

#### L'Infrastruttura in YAML (.github/workflows/ci.yml)

Abbiamo programmato un server senza toccarlo fisicamente tramite un file YAML e come visto la sintassi YAML è spietata: usa l'indentazione e delle keyword specifiche. Un TAB al posto di due spazi farà schiantare il server

L'anatomia della nostra pipeline:

1. **Il Trigger (on: [push]):** L'evento che fa partire l'automazione

2. **L'Ambiente (runs-on: ubuntu-latest):** Il sistema operativo sterile

3. **I Passi (steps):** Script sequenziali. Prima usiamo actions preconfezionate per scaricare il codice (checkout) e installare l'interprete (setup-python). Poi passiamo al terminale puro tramite il blocco run per lanciare pip install e pytest

**⚠️ LA REGOLA DEL COLLAUDO:** Se la pipeline esplode (pallino rosso), è vietato andare a tentativi. L'unica azione da compiere è aprire i log del server su GitHub, leggere gli errori e risolverli

---

## 2. Il Cambio di Paradigma: Verso il Black Box

Fino ad oggi abbiamo lavorato con il microscopio (White Box Testing): importato le funzioni, contato gli if e mockato le dipendenze. È potente, ma fragile: se stravolgete la logica interna (es. cambiando un if in un match/case), i test si rompono anche se l'output finale è identico

Oggi abbiamo buttato il microscopio. Con il Black Box Testing trattiamo il programma come una scatola nera inespugnabile. Non importiamo codice. Inseriamo un input dal terminale e pretendiamo un output. Se il contratto verso l'esterno è rispettato, il test passa. Questa architettura vi rende invulnerabili ai refactoring interni

---

## 3. Il Contratto di Sistema e lo Standard POSIX

Non facciamo Black Box Testing testando stringhe a caso. Seguiamo lo standard universale che fa comunicare i linguaggi di programmazione con i sistemi operativi

Negli anni '80 i sistemi operativi erano incompatibili tra loro. L'IEEE ha creato lo standard POSIX (Portable Operating System Interface) come trattato di pace. Ha standardizzato i canali di comunicazione che ogni ingegnere deve conoscere:

- **Standard Output (stdout):** Il flusso di testo per i risultati andati a buon fine

- **Standard Error (stderr):** Il flusso di testo dedicato esclusivamente alla diagnostica e agli errori

- **Gli Exit Code (Codici di Uscita):** I sistemi operativi e le CI/CD (come GitHub Actions) sono stupidi. Non leggono i vostri print("Errore"). Leggono solo un numero da 0 a 255.

## La Semantica degli Exit Code (Tramite sys.exit())

- **0 (Il Successo):** Lo zero assoluto. Comunica al sistema operativo: "Transazione pulita, procedi"

- **1 (Errore Generico):** Fallimento di base. L'utente ha dimenticato un parametro o c'è un errore di forma

- **2 (Errore di Business):** L'input era corretto formalmente, ma violava una regola aziendale o di sicurezza (es. tentato accesso con l'utente riservato 'admin')

Avere codici di uscita diversi permette ai sistemisti di scrivere script di automazione che reagiscono in modo diverso in base a come il vostro programma è fallito. Voi non scrivete codice solo per gli umani, lo scrivete per altre macchine.

---

## 4. Disaccoppiamento Totale (subprocess)

Per testare la nostra scatola nera senza mai usare l'import, abbiamo usato la libreria nativa subprocess. Questo strumento permette al nostro file di test di orchestrare il sistema operativo simulando un utente che digita nel terminale

```python
# L'anatomia di una chiamata di sistema in Python
risultato = subprocess.run(["python", "generatore.py", "giovanni"], capture_output=True, text=True)

# L'asserzione del contratto:
assert risultato.returncode == 0   # Pretendo che l'Exit Code sia di successo
assert "GIOVANNI" in risultato.stdout # Pretendo che il risultato sia su stdout
```

Se domani cambiate tutte le variabili interne di generatore.py, finché restituite 0 al sistema operativo e il testo corretto, i test continueranno a passare. Questo è un Quality Gate inespugnabile

---

## 5. Documentazione Ufficiale (RTFM)

Come sempre non indovinate la sintassi ma leggete la documentazione:

- **GitHub Actions (Concetti chiave):** docs.github.com/en/actions/learn-github-actions/understanding-github-actions

- **Continuous Integration:** https://docs.github.com/en/actions/get-started/continuous-integration

- **Python sys.argv ed exit():** docs.python.org/3/library/sys.html

- **Python subprocess:** docs.python.org/3/library/subprocess.html

- **POSIX Exit Codes:** tldp.org/LDP/abs/html/exitcodes.html e https://www.ditig.com/linux-exit-status-codes

- **Martin Fowler sulla Test Pyramid:** martinfowler.com/articles/practical-test-pyramid.html Il manifesto architetturale su quanti test isolati e quanti test Black Box/Integrazione un'azienda dovrebbe avere
