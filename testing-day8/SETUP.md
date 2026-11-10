# SETUP — Giorno 8: il corriere, poi il browser

> 📖 Una parola non vi è chiara? Cercatela in [`CONCETTI_BASE.md`](../CONCETTI_BASE.md), il dizionario del corso.

> ⏰ **Si riparte dal compito**: la prima parte della mattina correggiamo insieme il Lab 3 della G1 ([`testing-day6/lab3_dipendenze_esterne/README.md`](../testing-day6/lab3_dipendenze_esterne/README.md)): il mock del corriere, il timeout, l'eccezione di dominio. Servono **corriere e app accesi** (punto 3).
>
> Poi passiamo al browser. Se a casa **non** avete installato Playwright, lanciate **appena arrivati** i comandi del punto 2: il download è lungo e va avanti da solo mentre correggiamo il compito.

Oggi lavorate sullo **stesso repository** della Bottega.

## 1. Il punto di partenza

Lavorate sul vostro repository, su un branch nuovo:

```bash
git switch -c g3
```

**Il vostro compito non è finito, o il codice è in disordine?** In `testing-day8/bottega_start/` c'è la Bottega con le correzioni dei Lab 1, 2 e 3 già applicate (la pubblico la mattina della lezione: fate `git pull`). Copiatela **fuori** dalla cartella del corso, mettetela sotto Git e copiateci la vostra cartella `tests/`.

> Il frontend (`static/`) in `bottega_start/` è quello **originale**, con i suoi difetti: oggi lo correggete voi.

## 2. Le dipendenze nuove

Con il venv attivo:

```bash
pip install pytest-playwright==0.10.0 playwright==1.64.1 axe-playwright-python==0.1.8
python -m playwright install chromium
```

Aggiungete le tre righe a `requirements.txt` (le trovate già in `bottega_start/requirements.txt`).

> ⚠️ **Consigliato:** in `tests/conftest.py` date alla fixture `base_url` lo scope di sessione:
>
> ```python
> @pytest.fixture(scope="session")      # prima era solo @pytest.fixture
> def base_url():
>     return "http://localhost:8000"
> ```
>
> Perché: Playwright usa `base_url` per i test con il browser e la vuole "di sessione", cioè calcolata una volta per tutta la sessione. Se un test con il browser (fixture `page`) trova una `base_url` "per ogni test" (lo scope di default), si ferma con `ScopeMismatch`. Succede, per esempio, se mettete un test con il browser direttamente in `tests/` invece che in `tests/e2e/`, accanto al `conftest.py` del lab. I test delle API e quelli con il mock **non** ne sono toccati. (Nelle soluzioni pubblicate lo scope è già di sessione.) Se avete installato Playwright a casa, il primo comando allinea le versioni a quelle del corso e il secondo scarica il browser solo se manca.

Verifica:

```bash
python -m playwright --version          # Version 1.64.1
pytest -VV                              # tra i plugin deve comparire pytest-playwright-0.10.0
```

### Piano B: il download del browser non va

Il browser di Playwright pesa qualche centinaio di MB e la rete dell'aula, con 20 persone insieme, soffre. Se `playwright install chromium` non finisce, potete usare il **Chrome o Edge già installato** sul vostro PC (va scaricato solo il pacchetto Python):

```bash
pytest tests/e2e --browser-channel chrome      # Google Chrome installato
pytest tests/e2e --browser-channel msedge      # Microsoft Edge (preinstallato su Windows)
```

Per non doverlo scrivere ogni volta, aggiungetelo in `pytest.ini`, alla riga `addopts`: `addopts = -m "not chaos" --browser-channel chrome`.

## 3. Accendete il sistema

Due terminali con il venv attivo, nella cartella `bottega/`:

| Terminale | Comando |
|-----------|---------|
| 1 | `python corriere.py` |
| 2 | `python app.py` |

Aprite http://localhost:8000 e fate un acquisto a mano. Teneteli accesi tutto il giorno: servono ai test delle API, al registratore (`codegen`) e alla pagina. I test con il browser li riusano (se li trovano spenti, li accendono da soli).

## 4. Il primo segno di vita

Nel terzo terminale (lo facciamo insieme quando passiamo al browser):

```bash
python -m playwright codegen localhost:8000
```

Si aprono due finestre: un browser e il **Playwright Inspector**. Fate login e aggiungete un prodotto: il codice Python si scrive da solo. Chiudete tutto quando avete visto il codice comparire.

## Problemi frequenti

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| `Executable doesn't exist at .../ms-playwright/...` | Il browser non è stato scaricato, o è di un'altra versione di Playwright | `python -m playwright install chromium`, oppure il piano B |
| `ScopeMismatch: You tried to access the function scoped fixture base_url with a session scoped request object` | Un test con il browser usa una `base_url` senza `scope="session"` (di solito: il test non è in `tests/e2e/`) | Spostate il test in `tests/e2e/`, oppure il riquadro ⚠️ del punto 2 |
| `fixture 'page' not found` | `pytest-playwright` non è installato in **questo** venv | `pip install pytest-playwright==0.10.0` con il venv attivo |
| `playwright: command not found` | La cartella degli script del venv non è nel PATH | Usate sempre `python -m playwright ...` |
| Su Linux / WSL: mancano librerie di sistema | Il browser ha bisogno di librerie che il sistema non ha | `python -m playwright install --with-deps chromium` |
| `Address already in use` | Avete lanciato `app.py` due volte | Chiudete il secondo terminale: i test riusano il server già acceso |
