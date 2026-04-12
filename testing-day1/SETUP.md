# Setup dell'Ambiente di Lavoro

Per eseguire il codice di questo corso, hai bisogno di Python 3.10+ e di un ambiente virtuale isolato. Segui le istruzioni per il tuo sistema operativo.

## 1. Installazione di Python

### 🪟 Windows 10 (Standard di Laboratorio)

1. Vai su [python.org/downloads](https://www.python.org/downloads/) e scarica l'installer per Windows.
2. **ATTENZIONE - PASSAGGIO CRITICO:** Quando avvii l'installer, prima di cliccare "Install Now", **DEVI spuntare la casella "Add python.exe to PATH"** in basso. Se non lo fai, il terminale non troverà i comandi.
3. Clicca "Install Now" e attendi la fine.
4. Apri PowerShell e verifica l'installazione digitando:
   `python --version`

_(Nota: Evita di installare Python dal Microsoft Store, causa problemi di permessi con i virtual environment)._

### 🍎 macOS

1. I Mac moderni non hanno Python preinstallato. Il modo migliore per gli sviluppatori è usare Homebrew.
2. Apri il Terminale e installa Homebrew (se non lo hai già):
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Installa Python:
   `brew install python`
4. Verifica:
   `python3 --version`

### 🐧 Linux (Ubuntu/Debian)

1. Apri il terminale.
2. Esegui l'aggiornamento e installa Python, pip e il pacchetto venv:
   `sudo apt update`
   `sudo apt install python3 python3-pip python3-venv`
3. Verifica:
   `python3 --version`

---

## 2. Inizializzazione del Progetto (Obbligatorio)

Ricordate: Non si installano MAI le librerie a livello globale. Creeremo un ambiente virtuale (`venv`) isolato per questo corso.

1. Apri il terminale dentro la cartella del progetto che hai clonato (`ifts-testing-day1`).
2. Crea l'ambiente virtuale:

   - **Windows:** `python -m venv venv`
   - **macOS/Linux:** `python3 -m venv venv`

3. Attiva l'ambiente virtuale:

   - **Windows:** `.\venv\Scripts\activate`
     _(Se ricevi un errore rosso sui criteri di esecuzione, lancia questo comando prima: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`)_
   - **macOS/Linux:** `source venv/bin/activate`

4. Se vedi `(venv)` apparire all'inizio della riga del tuo terminale, sei dentro l'ambiente isolato.

Sei pronto per lavorare.
