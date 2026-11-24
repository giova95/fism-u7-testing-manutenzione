# SETUP — Giorno 10: Chaos Engineering Game Day

> 📖 Una parola non vi è chiara? Cercatela in [`CONCETTI_BASE.md`](../CONCETTI_BASE.md), il dizionario del corso.

> **Se riuscite, fatelo a casa prima di mercoledì** (un quarto d'ora). Dopo l'esame si riparte direttamente con il pomeriggio, e la rete dell'aula non regge 20 `pip install` insieme. Chi non ce la fa lo farà alla ripresa, in coppia con un compagno che l'ha già fatto.

Oggi pomeriggio non lavorate sul vostro repository della Bottega: lavorate tutti su **`bottega_start`**, una copia comune e già pronta. Così, durante il Game Day, tutte le squadre partono dallo stesso sistema e nessuno è penalizzato da un compito rimasto a metà. (Nei compiti porterete le difese nel vostro repository.)

## 1. Prendete `bottega_start`

Copiate la cartella `testing-day10/bottega_start/` del repository del corso in una posizione vostra, **fuori** dal vostro repository della Bottega, e rinominatela `bottega_g5`. Poi:

```bash
cd bottega_g5
git init
git add .
git commit -m "chore: punto di partenza della G5"
```

Cosa c'è di nuovo rispetto alla Bottega che conoscete (le correzioni del Lab 3 sul corriere, che abbiamo fatto insieme, sono già dentro: timeout, eccezione di dominio, 503):

| File | Cosa fa |
|------|---------|
| `chaos.py` | il **chaos middleware**: prima di ogni richiesta può rallentare o rompere apposta un endpoint |
| `chaos_ctl.py` | il telecomando del caos (inietta, stato, stop, orologio, corriere) |
| `misura.py` | misura lo **stato stazionario**: tasso di errore, latenza p50 e p95 per endpoint |
| `tests/test_smoke.py` | smoke test del flusso critico (catalogo veloce, acquisto completo) |
| `static/app.js` | il frontend ora mostra gli errori invece di "non fare niente" |

## 2. Il recinto (virtual environment)

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Nella lista c'è una libreria nuova, **`tenacity`**: serve solo per la parte facoltativa del compito.

## 3. Accendete il sistema: TRE terminali, venv attivo in tutti

| Terminale | Comando | Chi è |
|-----------|---------|-------|
| 1 | `python chaos_ctl.py corriere` | SpediVeloce, il corriere esterno (NON è nostro) |
| 2 | `python app.py` | La Bottega |
| 3 | (libero) | test, misure, comandi |

> Da oggi il corriere si avvia con `python chaos_ctl.py corriere`: fa la stessa cosa di `python corriere.py`, ma accetta `--latenza` e `--errori` con la **stessa sintassi su Mac e Windows** (niente più `$env:...` in PowerShell).

## 4. Verifica (nel terminale 3)

```bash
python chaos_ctl.py stato
```
→ deve stampare `Nessun guasto attivo.`

```bash
pytest
```
→ `3 passed, 1 deselected`

```bash
python misura.py
```
→ deve terminare con `VERDETTO: ipotesi VERIFICATA`.

Se tutte e tre le verifiche vanno, siete pronti. Se no, segnatevi l'errore e mostratelo al docente alla ripresa: si sistema in coppia.

## Problemi frequenti

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| `La Bottega (http://localhost:8000) non risponde` | `app.py` è spento | Terminale 2: `python app.py` |
| `Address already in use` | Un altro processo occupa la porta 8000 o 8001 | Mac: `lsof -i :8000` e `kill <PID>` · Windows: `netstat -ano \| findstr :8000` e `taskkill /PID <PID> /F` |
| `ModuleNotFoundError: tenacity` | `pip install` fatto in un altro venv | Attivate il venv **di bottega_g5** e rifate `pip install -r requirements.txt` |
| `misura.py` ci mette più di un minuto | Il corriere è stato avviato con una latenza | Terminale 1: CTRL+C e `python chaos_ctl.py corriere` senza opzioni |
| Dopo `misura.py` il browser vi ha "sloggato" | `misura.py` chiama `/api/reset` per ripartire da dati puliti | Rifate il login: è normale |
