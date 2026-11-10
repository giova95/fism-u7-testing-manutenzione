# LAB 2 — Report che si leggono

> 📖 **Parole da sapere per questo lab** (spiegate con esempi in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [pipeline CI/CD](../../CONCETTI_BASE.md#pipeline-cicd) · [ambiente](../../CONCETTI_BASE.md#ambiente-sviluppo-test-produzione)

## Contesto

Lanciate `pytest -v`: escono righe e righe di nomi di test, puntini, lettere. Per voi è chiaro. Ora immaginate di mandare quell'output alla CTO con scritto: «Possiamo andare in produzione venerdì?». Non lo leggerà.

Lo stesso risultato serve a tre pubblici diversi, e ognuno ha bisogno del suo formato:

| Chi legge | Cosa gli serve | Formato | Comando |
|-----------|----------------|---------|---------|
| **Macchine** (CI, dashboard, altri strumenti) | dati standard | JUnit XML | `pytest --junitxml=...` |
| **Sviluppatori e QA** | dettaglio, filtri, errori completi | un file HTML | `pytest --html=...` (plugin `pytest-html`) |
| **Chi decide** (CTO, cliente) | 30 secondi: si va o no? con quali rischi? | una pagina | il Test Report, scritto a mano (compito) |

In aula li vediamo prodotti in locale (Livello 1). Farli produrre alla pipeline è il Livello 2. Il terzo, il Test Report di una pagina, lo scrivete a casa: è il Livello 1 del compito.

**File da usare:** `testing-day9/lab2_reporting/test_difetti_noti.py` → copiatelo nella cartella `tests/` del vostro repository.
**Prerequisito:** `python corriere.py` e `python app.py` accesi in due terminali, venv attivo.

## Livello 1: Sopravvivenza (obbligatorio per tutti, ~20 minuti)

### 1. Il plugin dei report

Se partite da `bottega_start/` lo avete già. Altrimenti:

```bash
pip install pytest-html==4.2.0
```

(Nel Livello 2 lo scriviamo anche in `requirements-dev.txt`, così lo installa la pipeline.)

### 2. I difetti noti diventano test

Aprite `test_difetti_noti.py` e leggetelo. Ci sono due marcatori nuovi:

| Marcatore | Significato | Nell'output |
|-----------|-------------|-------------|
| `@pytest.mark.xfail(strict=True, reason="BUG-009 ...")` | «So che fallisce: è un difetto **registrato**, con un ID e un motivo» | `x` (xfailed) |
| ...e se un giorno quel test **passa** | il difetto è stato corretto e il registro è vecchio: con `strict=True` la suite diventa **rossa** | `X` (XPASS) → rosso |
| `@pytest.mark.skip(reason="...")` | «Oggi questo controllo non si può fare, ed ecco perché» | `s` (skipped) |

Lanciate:

```bash
pytest -rxXs
```

L'opzione `-rxXs` aggiunge in fondo un riepilogo con i **motivi** di xfail (`x`), XPASS (`X`) e skip (`s`).

**Domanda:** che differenza c'è tra un test rosso e un test `xfail`? Per chi legge il report, cambia qualcosa?

> Se un giorno correggete `BENVENUTO10` (è il ticket BOT-42 del Lab 1, nel compito facoltativo), quel test vi darà **XPASS → rosso**. Non è un errore: è il meccanismo che funziona. Togliete il decoratore `xfail` da quel test: il registro dei difetti ha una voce in meno.

### 3. Il report per i tecnici

```bash
pytest --html=report/report.html --self-contained-html
```

Apritelo:

```bash
# Mac
open report/report.html
# Windows (PowerShell)
start report/report.html
```

Cliccate sui filtri in alto (Passed, Failed, Skipped, Expected failures...) e aprite il dettaglio di un test. `--self-contained-html` mette CSS e JavaScript **dentro** il file: si può allegare a un ticket o a una mail, come un PDF.

### 4. Il report per le macchine

```bash
pytest --junitxml=report/junit.xml
```

Apritelo con l'editor. Per voi è scomodo da leggere, ed è giusto così: è uno **standard** che capiscono GitHub, GitLab, Jenkins e decine di altri strumenti. Non si scrive per gli umani, si scrive per **altre macchine**.

> I report sono **prodotti** dai test, non si committano: controllate che nel vostro `.gitignore` ci sia la riga `report/` (in `bottega_start/` c'è già). Li produce la pipeline a ogni push (Livello 2).

> 🧩 **Non sai da dove partire?** Il Livello 1 sono tre comandi, dalla cartella del progetto, con il venv attivo e i due server accesi. Copiateli e sostituite i `???` (le risposte sono nei punti 2-4 qui sopra):
>
> ```bash
> # 2. difetti noti: riepilogo finale con i MOTIVI di xfail (x), XPASS (X) e skip (s)
> pytest -r???
>
> # 3. report per i tecnici: un solo file HTML, con CSS e JavaScript dentro
> pytest --html=report/???.html --???
>
> # 4. report per le macchine: lo standard JUnit
> pytest --???=report/junit.xml
> ```
>
> Poi compilate questa tabella guardando l'ultima riga dell'output del punto 2 (vi serve per il Test Report del compito):
>
> | passed | failed | xfailed | skipped |
> |-------:|-------:|--------:|--------:|
> | ??? | ??? | ??? | ??? |
>
> **Trucchi:**
> - se l'output finisce con `Il server ... è spento`, non è un problema dei report: manca `python app.py` (o `python corriere.py`) in un altro terminale;
> - `fixture 'auth' not found`: il vostro `tests/conftest.py` non ha la fixture `auth`. Copiate `tests/conftest.py` da `testing-day9/bottega_start/`;
> - `unrecognized arguments: --html`: manca il plugin, rifate il punto 1 con il venv attivo.

## Livello 2: Ingegneria — i report nella pipeline (nel laboratorio del pomeriggio se c'è tempo, altrimenti a casa)

Il runner di GitHub Actions viene **distrutto** a fine job: un report scritto lì sparisce con lui. Per tenerlo bisogna caricarlo come **artifact**, un file allegato alla run che si scarica dalla sua pagina.

### 0. Avete una pipeline?

Se nel vostro repository **non** c'è `.github/workflows/pipeline.yml` (o non è verde), copiate da `testing-day9/bottega_start/` nella radice del vostro repository questi quattro file:

| File | A cosa serve |
|------|--------------|
| `.github/workflows/pipeline.yml` | la pipeline: accende corriere e Bottega, lancia i test |
| `requirements.txt` | le dipendenze di **produzione** (flask, requests, gunicorn) |
| `requirements-dev.txt` | `-r requirements.txt` + pytest e gli strumenti di test, compreso `pytest-html` |
| `.python-version` | una riga: `3.14` |

Se nel vostro vecchio `requirements.txt` c'erano righe di Playwright o axe (G3), spostatele in `requirements-dev.txt`. Poi `pip install -r requirements-dev.txt`, commit e push su `develop`: la pipeline deve essere **verde** prima di andare avanti. Questi stessi file servono anche per il deploy del Lab 3.

### 1. Lo step dei test genera i report

Nella pipeline, sostituite lo step che lancia pytest con:

```yaml
      - name: Eseguo i test e genero i report
        run: >-
          pytest -v --ignore=tests/e2e
          --junitxml=report/junit.xml
          --html=report/report.html --self-contained-html
```

(`>-` vuol dire: le righe che seguono sono **un solo comando**, spezzato per leggerlo meglio. `--ignore=tests/e2e`: i test del browser in CI richiederebbero Playwright e i browser installati nel runner.)

### 2. I report si scaricano dalla pagina della run

Aggiungete in fondo al job `test`:

```yaml
      - name: Carico i report (scaricabili dalla pagina della run)
        if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v7
        with:
          name: report-test
          path: |
            report/
            *.log
          retention-days: 14
```

- `if: ${{ !cancelled() }}`: lo step gira **anche se i test sono falliti**. È proprio quando falliscono che il report serve. Senza `if`, uno step dopo un fallimento viene saltato.
- Le `${{ }}` sono obbligatorie: in YAML un valore che comincia con `!` ha un significato speciale e il workflow non parte nemmeno.
- `*.log`: i log di gunicorn. Se la Bottega si è rotta dentro il runner, la traccia è lì.

Push su `develop`, aprite la run su GitHub: in fondo alla pagina c'è la sezione **Artifacts**. Scaricate lo zip, estraetelo e aprite `report.html`.

> 🧩 **Non sai da dove partire?** Ecco come deve finire il job `test`. Le righe sopra (`checkout`, `setup-python`, installazione, accensione dei server) restano quelle che avete. Sostituite i `???`:
>
> ```yaml
>       - name: Eseguo i test e genero i report
>         run: >-
>           pytest -v --ignore=tests/e2e
>           --junitxml=report/???.xml
>           --html=report/report.html --???
>
>       - name: Carico i report (scaricabili dalla pagina della run)
>         if: ${{ ???() }}                 # deve girare anche se i test falliscono
>         uses: actions/upload-artifact@v7
>         with:
>           name: report-???
>           path: |
>             ???/
>             *.log
>           retention-days: 14
> ```
>
> **Trucco:** gli step stanno tutti allo **stesso rientro** (6 spazi prima di `- name:`). Se la run si ferma subito con *Invalid workflow file*, quasi sempre è il rientro.

## Livello 3: Escalation (per chi vuole andare oltre, anche a casa)

1. **La tabella nella pagina della run.** Ogni step può scrivere Markdown nel file indicato dalla variabile `$GITHUB_STEP_SUMMARY`: GitHub lo mostra in cima alla pagina della run. Scrivete `scripts/riepilogo_ci.py`, che legge `report/junit.xml` e stampa una tabella (passati, falliti, difetti noti, saltati) con, sotto, nome e motivo di ogni test fallito e di ogni difetto noto. Regole:
   - lo script **racconta** l'esito, non lo decide: esce sempre con 0 (l'esito resta l'exit code di pytest);
   - se `junit.xml` non esiste (pytest si è fermato prima), lo dice invece di andare in errore.

   Indizio: `xml.etree.ElementTree`; ogni `<testcase>` può contenere `<failure>`, `<error>` o `<skipped>`, e gli xfail sono `<skipped type="pytest.xfail">`. Nella pipeline:

   ```yaml
         - name: Riepilogo nella pagina della run
           if: ${{ !cancelled() }}
           run: python scripts/riepilogo_ci.py report/junit.xml >> "$GITHUB_STEP_SUMMARY"
   ```

2. **Un report con un titolo e una versione.** In `tests/conftest.py` aggiungete la funzione `pytest_html_report_title(report)` che imposta `report.title`, e nella pipeline passate `--metadata Commit "$GITHUB_SHA"`. Perché un report senza versione vale poco?
3. **La coverage in HTML, e il mistero dello 0%.** Lanciate `pytest --cov=. --cov-report=html:report/coverage` e aprite `report/coverage/index.html`. Più di 30 test chiamano `app.py` via HTTP: perché la sua coverage è **0%**? (Indizio: in quale **processo** gira `app.py`? E in quale gira pytest?) Poi provate ad avviare il server dentro coverage: `BOTTEGA_ENV=test coverage run --source=app,spedizioni,preventivo app.py`, lanciate i test in un altro terminale, fermate il server con CTRL+C e `coverage html -d report/coverage-server`.

## Documentazione

- pytest, output e opzione `-r`: https://docs.pytest.org/en/stable/how-to/output.html
- pytest, skip e xfail: https://docs.pytest.org/en/stable/how-to/skipping.html
- pytest-html: https://pytest-html.readthedocs.io/en/latest/
- GitHub Actions, artifact: https://docs.github.com/en/actions/tutorials/store-and-share-data
- actions/upload-artifact: https://github.com/actions/upload-artifact
- GitHub Actions, job summary (`$GITHUB_STEP_SUMMARY`): https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-job-summary
- pytest-cov: https://pytest-cov.readthedocs.io/en/latest/
