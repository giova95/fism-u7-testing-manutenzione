# Lab 2: Il Firewall CLI

## Contesto Aziendale

Siete stati assegnati al team di Sicurezza Infrastrutturale. Il vostro compito è sviluppare e testare un simulatore di Firewall da riga di comando. Questo script Python verrà eseguito dai server Linux per decidere se autorizzare o bloccare una connessione in entrata.
Non dovete testare il codice "da dentro", dovete testarlo dal sistema operativo, catturando gli Exit Code e gli stream di errore.

## Task

### Step 1: Le Specifiche del Contratto

Create il file `firewall.py`, dovete scriverlo voi da zero usando sys.argv, sys.exit, sys.stderr e sys.stdout (tramite print)

Il programma deve essere richiamato dal terminale in questo modo:
`python firewall.py <INDIRIZZO_IP> <RUOLO>`

**Requisiti:**

1. **Parametri Mancanti:** Se l'utente non passa esattamente due parametri (IP e Ruolo), il programma deve stampare su standard error: "ERRORE CRITICO: IP e Ruolo obbligatori." e terminare con Exit Code 1.

2. **Blacklist:** Se l'IP inserito è "199.0.0.1", il programma deve bloccare l'accesso. Stampa su standard error: "MINACCIA RILEVATA: IP in blacklist." e termina con Exit Code 2.

3. **Privilegi Root:** Se il ruolo richiesto è "root", può essere accettato SOLO se l'IP è "10.0.0.1" (Rete interna). Se qualcuno tenta l'accesso root da un altro IP, stampa su standard error: "VIOLAZIONE: Root permesso solo da rete interna." e termina con Exit Code 3.

4. **Accesso Consentito:** Se nessuna delle regole precedenti viene infranta, stampa su standard output: "AUTORIZZAZIONE CONCESSA: [RUOLO] - [INDIRIZZO_IP]" e termina con Exit Code 0.

### Step 2: La Suite Black Box

Create il file test_firewall.py
⚠️REGOLA TASSATIVA: È severamente vietato scrivere import firewall. Siete ispettori esterni.
Scrivete una suite di test usando la libreria nativa subprocess.

Dovete scrivere un test isolato per coprire ognuno dei 4 requisiti descritte allo step 1

Ogni test deve asserire due cose:

- Che l'Exit Code (returncode) sia esattamente quello previsto dallo standard.

- Che la stringa di testo restituita in stdout o stderr contenga il messaggio esatto.

Suggerimento: Per eseguire il processo, usate subprocess.run

### Step 3: Il Quality Gate in Cloud

Il vostro computer non ha autorità. Portate tutto nel cloud.

1. Create il file requirements.txt (basta inserire pytest). Non usiamo pytest-cov questa volta, perché testando da fuori (subprocess) la copertura interna non è tracciabile con i metodi base.

2. Create .github/workflows/ci.yml.

3. Scrivete lo YAML (usate quello dell'homework precedente, rimuovendo semplicemente la parte della --cov).

4. Eseguite git add ., git commit -m "feat: implementazione firewall e black box testing", git push.

5. Andate su GitHub Actions e assicuratevi che il pallino sia VERDE.

### Step 4: Fix improvvisa

La pipeline è verde. Il sistema è in produzione. Irrompe il CISO (Chief Information Security Officer):
"Ieri abbiamo avuto una compromissione. Dobbiamo bloccare immediatamente tutto il traffico proveniente dall'IP 8.8.8.8. Aggiungetelo alla blacklist e mandatelo online."

1. Aprite firewall.py. Modificate la regola 2 (Blacklist) affinché intercetti SIA l'IP "199.0.0.1" SIA "8.8.8.8".

2. Errore Volontario: Siete nel panico, quindi fate la modifica al codice, ma vi dimenticate di aggiornare i test.

3. Eseguite il push in produzione.

4. Andate su GitHub Actions. Guardate la build esplodere (Pallino ROSSO).

5. Aprite il log del server. Capite perché si è rotto, tornate in locale, scrivete il test mancante per verificare che 8.8.8.8 restituisca Exit Code 2, pushate e riportate la build in VERDE.

### REMINDER

Per questo homework non è prevista la consegna ma è fortemente consigliato lo svolgimento in vista della prova finale
