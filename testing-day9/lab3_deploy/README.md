# LAB 3 — L'ultimo miglio: dal push alla produzione

> 📖 **Parole da sapere per questo lab** (spiegate con esempi in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [deploy](../../CONCETTI_BASE.md#deploy) · [cloud / PaaS](../../CONCETTI_BASE.md#cloud--paas) · [variabile d'ambiente](../../CONCETTI_BASE.md#variabile-dambiente) · [segreto](../../CONCETTI_BASE.md#segreto-secret) · [pipeline CI/CD](../../CONCETTI_BASE.md#pipeline-cicd) · [smoke test](../../CONCETTI_BASE.md#smoke-test)

## Contesto

Nel semestre 1 la pipeline si fermava a un pallino verde: **Continuous Integration**. Il codice era *pronto*, ma poi qualcuno doveva copiarlo a mano su un server, di solito il venerdì sera. È lì che si rompe la produzione.

Oggi la pipeline arriva fino in fondo:

```
 push su develop ──▶ [ test ]                                   (solo test)
 push su main    ──▶ [ test ] ──verde──▶ [ deploy ] ──▶ Render ──▶ la Bottega è online
                        │
                      rosso ──▶ niente deploy
```

| Termine | Cosa significa |
|---------|----------------|
| **Continuous Integration** | ogni push viene testato in automatico (semestre 1) |
| **Continuous Delivery** | ogni versione verde è *pronta* per la produzione, ma il rilascio lo decide una persona con un click |
| **Continuous Deployment** | ogni versione verde su `main` va in produzione **da sola** (oggi) |

Avete appena visto il docente farlo sul suo repository. Ora lo rifate sul vostro, seguendo la traccia passo per passo.

**Prerequisito:** la **Parte A** di `SETUP_RENDER.md` (account Render collegato al repository), da fare a casa la sera prima. **Senza account** oggi non potete deployare: lavorate in coppia con chi ce l'ha (chi legge la traccia ad alta voce è utile quanto chi esegue), poi a casa fate la Parte A e questa traccia. È il Livello 1 del compito.

## Livello 1: la traccia guidata (a casa, facoltativa: è il Livello 2 del compito)

Ogni passo finisce con una **verifica**. Non andate avanti finché la verifica non torna.

### Passo 1 · Il repository è pronto per la produzione (20-25 minuti)

Se nel Lab 2 avete già copiato i quattro file da `bottega_start/` (Livello 2, punto 0), saltate alla parte su `app.py` qui sotto. Altrimenti copiate da `testing-day9/bottega_start/` nella **radice** del vostro repository:

| File | Perché serve in produzione |
|------|----------------------------|
| `requirements.txt` | solo ciò che serve all'app: flask, requests e **gunicorn**. Lo installa Render. pytest in produzione è peso inutile |
| `requirements-dev.txt` | `-r requirements.txt` + pytest e gli strumenti di test. Lo installate voi e la CI |
| `.python-version` | una riga, `3.14`: la leggono sia Render sia GitHub Actions |
| `.github/workflows/pipeline.yml` | la pipeline con il job `test` (lo completiamo al passo 4) |

Se nel vostro vecchio `requirements.txt` c'erano righe di Playwright o axe (G3), spostatele in `requirements-dev.txt`.

**gunicorn.** `python app.py` avvia il server di **sviluppo** di Flask, che non è fatto per Internet. In produzione si usa `gunicorn app:app`: "nel file `app.py`, prendi la variabile `app`". gunicorn **non funziona su Windows**: non importa, lo usano Render e la CI, che girano su Linux. In locale continuate con `python app.py`.

**«Quale versione sta girando?»** Una volta online, vorrete sapere **quale commit** è in produzione. Render lo scrive nella variabile d'ambiente `RENDER_GIT_COMMIT`. In `app.py` aggiungete una riga sotto `AMBIENTE = ...` e cambiate il `return` di `health()` (in `bottega_start/app.py` è già fatto, cercate `[G4]`):

```python
AMBIENTE = os.getenv("BOTTEGA_ENV", "sviluppo")
VERSIONE = os.getenv("RENDER_GIT_COMMIT", "locale")[:7]        # <- riga nuova

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "ambiente": AMBIENTE, "versione": VERSIONE})
```

In locale `/api/health` risponderà `"versione": "locale"`; su Render, i primi 7 caratteri del commit. È una modifica al **contratto**: copiate anche `README.md` da `bottega_start/` (contratto v1.1), o aggiungete voi la riga su `versione`. Un campo **in più** non rompe chi usa già l'endpoint; un campo in meno sì.

Controllate anche che in `app.py` ci sia il controllo che vieta il reset in produzione (`if AMBIENTE == "produzione": ... 403` dentro `reset()`): c'è dalla prima versione della Bottega, ma se l'avete toccato, rimettetelo.

```bash
git checkout develop
git add . && git commit -m "build: requirements di produzione, gunicorn, versione in /api/health"
git push
```

Quando la run su `develop` è verde, portate tutto su `main`, perché **Render legge `main`**: su GitHub, **Pull Request** `develop` → `main`, aspettate il verde, **Merge**. (Il job `deploy` non c'è ancora: per ora `main` viene solo testato.)

**Verifica:** su GitHub, scheda **Actions**: le run su `develop` e su `main` sono **verdi**. In locale, `http://localhost:8000/api/health` risponde con `"versione":"locale"`.

### Passo 2 · I due servizi su Render (15 minuti, più l'attesa della build)

Seguite `SETUP_RENDER.md`, **Parte B**, punti **B1** (corriere) e **B2** (Bottega). Mentre Render fa la build, non state fermi: leggete il passo 3.

**Verifica:**
- [ ] `https://corriere-<nome>.onrender.com/tariffa?cap=50100&peso=1` → `{"costo":4.9}`
- [ ] `https://bottega-<nome>.onrender.com/api/health` → `"ambiente":"produzione"` e una `versione` di 7 caratteri
- [ ] **Auto-Deploy Off** su entrambi i servizi (da adesso deploya solo la pipeline)

> Se il primo ordine online risponde **503**, non è un bug: il corriere stava dormendo, e mentre si svegliava non ha risposto come dovrebbe. La **vostra** gestione degli errori (l'eccezione di dominio e il 503) ha appena protetto la produzione: il sito è vivo e il carrello è salvo. Riprovate dopo un minuto.

### Passo 3 · Il deploy hook diventa un segreto (5 minuti)

Seguite `SETUP_RENDER.md`, punto **B3**: il secret `RENDER_DEPLOY_HOOK_URL` e le due variabili `PRODUZIONE_URL` e `CORRIERE_URL`.

> Se il job di deploy si ferma con `Malformed input to a URL function` o con «non è un deploy hook di Render», nel secret c'è il valore sbagliato (succede se tra copia e incolla avete copiato altro). Ricopiate l'URL da Render e aggiornate il secret.

**Verifica:** su GitHub, **Settings › Secrets and variables › Actions**: nella scheda **Secrets** c'è `RENDER_DEPLOY_HOOK_URL` (il valore non si vede più, è giusto così), nella scheda **Variables** ci sono i due URL.

### Passo 4 · Il job che deploya (10 minuti)

Aggiungete in fondo a `.github/workflows/pipeline.yml` un secondo job:

```yaml
  deploy:
    name: Deploy su Render
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Chiedo a Render di deployare ESATTAMENTE il commit testato
        env:
          DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK_URL }}
        run: |
          # Tolgo spazi e a capo: succede quando l'URL si copia a mano.
          HOOK="$(printf '%s' "$DEPLOY_HOOK" | tr -d '[:space:]')"
          if [ -z "$HOOK" ]; then
            echo "::error::Manca il secret RENDER_DEPLOY_HOOK_URL"
            exit 1
          fi
          case "$HOOK" in
            https://api.render.com/deploy/srv-*\?key=*) ;;
            *) echo "::error::RENDER_DEPLOY_HOOK_URL non è un deploy hook di Render: ricopialo da Render > Settings > Deploy Hook"
               exit 1 ;;
          esac
          curl --fail --silent --show-error --max-time 30 -X POST "${HOOK}&ref=${GITHUB_SHA}"
```

Non serve scriverlo a memoria: copiatelo così com'è, facendo attenzione al rientro. Riga per riga, il perché:

| Riga | Perché |
|------|--------|
| `needs: test` | il deploy parte **solo** se il job `test` è verde |
| `if: ... push ... main` | si deploya solo da `main`. `develop` e le Pull Request vengono testate ma **non** deployate (Git Flow) |
| `env: DEPLOY_HOOK: ${{ secrets... }}` | il segreto entra come variabile d'ambiente, mai scritto nel file. Nei log GitHub lo mostra come `***` |
| `tr -d '[:space:]'` | toglie spazi e a capo finiti nel secret per sbaglio durante il copia-incolla |
| `if [ -z ... ]` e `case ...` | se il secret manca, o non ha la forma di un deploy hook, un errore **chiaro** invece di un errore di curl difficile da capire |
| `&ref=${GITHUB_SHA}` | Render deploya **esattamente** il commit testato, non "l'ultimo che trova su main" |
| `--fail` | se Render risponde con un errore (401, 404...), lo step diventa rosso. Senza, curl stamperebbe l'errore e uscirebbe con 0, cioè "tutto bene" |
| `--max-time 30` | ogni chiamata di rete ha un timeout. Sempre |

> 🧩 **Non sai da dove partire?** Il problema di solito non è il job, ma **dove** metterlo: in YAML conta il rientro. Ecco lo scheletro del file dopo questo passo. Chiudete il blocco qui sopra e provate a sostituire i `???` usando solo la tabella "Riga per riga"; poi confrontate.
>
> ```yaml
> name: Pipeline Bottega
>
> on:
>   push:
>     branches: [main, develop]
>   pull_request:
>     branches: [main, develop]
>
> permissions:
>   contents: read
>
> jobs:
>   test:
>     # ... il job test che avete già: non si tocca
>
>   deploy:                         # stesso rientro di "test:" (2 spazi)
>     name: Deploy su Render
>     needs: ???                    # quale job deve essere verde prima?
>     if: github.event_name == '???' && github.ref == 'refs/heads/???'
>     runs-on: ubuntu-latest
>     steps:
>       - name: Chiedo a Render di deployare ESATTAMENTE il commit testato
>         env:
>           DEPLOY_HOOK: ${{ secrets.??? }}     # il nome del secret creato al passo 3
>         run: |
>           # ... le righe con HOOK, if e case: copiatele dal blocco qui sopra ...
>           curl --??? --silent --show-error --max-time ??? -X POST "${HOOK}&ref=${???}"
> ```
>
> **Trucco:** se dopo il push la run si ferma subito con *Invalid workflow file*, quasi sempre è il rientro. Se il job `deploy` compare **grigio** (saltato), la condizione `if` è falsa: su `develop` è giusto così; dopo il merge su `main` no (controllate che il branch si chiami davvero `main` e non `master`).

### Passo 5 · Il Git Flow fa partire il deploy (10 minuti)

```bash
git checkout develop
git add . && git commit -m "ci: deploy automatico su Render"
git push                                   # → solo test, deploy grigio
```

Su GitHub: **Pull Request** `develop` → `main`, aspettate il verde, **Merge**.

**Verifica finale:**
- [ ] nella run partita dal merge su `main`: `test` verde → `deploy` verde;
- [ ] su Render, nella pagina **Events** del servizio bottega, compare un deploy nuovo con lo SHA del vostro commit;
- [ ] dopo un paio di minuti `https://bottega-<nome>.onrender.com/api/health` risponde con `"ambiente":"produzione"` e con la `versione` uguale ai primi 7 caratteri del commit del merge (`git log --oneline -1 origin/main`);
- [ ] `curl -s -o /dev/null -w "%{http_code}\n" -X POST https://bottega-<nome>.onrender.com/api/reset` stampa **403**.

Se ci siete arrivati, avete fatto Continuous Deployment: nessuno ha toccato un server a mano.

## Livello 2: Ingegneria (a casa: Livello 3 del compito, facoltativo)

Il deploy hook risponde **subito** "ok, deploy avviato", ma la build e l'avvio richiedono minuti. Come fa la pipeline a sapere che la versione nuova è online, e configurata bene? Con gli **smoke test**: il test dell'elettricista, accendo e guardo se esce fumo. Pochi controlli, veloci, contro la **produzione vera**, senza modificare i dati.

### 1. «Quale versione sta girando?»

Lo avete già fatto al passo 1: `/api/health` risponde con la `versione`. È quello che permette allo smoke test di capire se in linea c'è già il commit nuovo o ancora quello vecchio.

### 2. Gli smoke test

Create la cartella `smoke/` (fuori da `tests/`, così non eredita la fixture che chiama `/api/reset`) con:

**`smoke/conftest.py`**: una fixture `url_produzione` con `scope="session"` che:
1. legge l'URL da `PRODUZIONE_URL` (se manca: `pytest.exit` con un messaggio chiaro);
2. interroga `/api/health` ogni 10 secondi, **ogni chiamata con timeout**, finché risponde 200 in JSON e `versione` è uguale ai primi 7 caratteri di `VERSIONE_ATTESA` (se la variabile è impostata);
3. se dopo `SMOKE_ATTESA_MAX` secondi (default 600) non ci è riuscito, `pytest.exit(..., returncode=1)` con l'ultimo stato visto.

È il timeout che conoscete, in grande: pazienza **sì**, ma con un **budget**. Una pipeline che aspetta per sempre è peggio di una pipeline rossa. (Durante il cold start Render può rispondere con una sua pagina HTML di attesa: non è ancora la Bottega, si aspetta.)

**`smoke/test_smoke.py`**: almeno questi controlli, **senza modificare i dati** della produzione:

| Controllo | Perché |
|-----------|--------|
| `/api/health` → `ambiente == "produzione"` | se manca `BOTTEGA_ENV` su Render, tutto il resto è sbagliato |
| `POST /api/reset` → **403** | altrimenti **chiunque** su Internet può cancellare il negozio |
| JSON rotto al login → **400** in JSON, nessun `Traceback` | il debugger non deve mai arrivare a un client |
| `/api/prodotti/abc` → 404 in JSON | gli errori restano JSON anche in produzione |

Provateli prima in locale, con l'app configurata come in produzione:

```bash
# Mac/Linux (terminale 1)
BOTTEGA_ENV=produzione gunicorn app:app --bind 127.0.0.1:8002
# terminale 2
PRODUZIONE_URL=http://127.0.0.1:8002 pytest smoke -v

# Windows (terminale 1): gunicorn non c'è, ma con BOTTEGA_ENV=produzione il debug è spento lo stesso
$env:BOTTEGA_ENV="produzione"; python app.py
# terminale 2
$env:PRODUZIONE_URL="http://127.0.0.1:8000"; pytest smoke -v
```

Poi contro Render: `PRODUZIONE_URL=https://bottega-<nome>.onrender.com pytest smoke -v -s` (`-s` mostra i messaggi di attesa).

### 3. Il job `smoke`

```yaml
  smoke:
    name: Smoke test in produzione
    needs: deploy
    runs-on: ubuntu-latest
    env:
      PRODUZIONE_URL: ${{ vars.PRODUZIONE_URL }}
      VERSIONE_ATTESA: ${{ github.sha }}
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version-file: ".python-version"
      - run: pip install -r requirements-dev.txt
      - name: Smoke test (aspetta build, avvio e cold start)
        timeout-minutes: 15
        run: pytest smoke -v -s
```

`timeout-minutes: 15` è la cintura di sicurezza **sopra** il budget della fixture: se qualcosa si pianta comunque, GitHub ferma il job.

### 4. Il documento di rilascio

In azienda si chiama **runbook**: il documento che usa chi è di turno quando la produzione è giù e voi non ci siete. Create `RILASCIO.md` nella radice del repository, con sei sezioni:

1. **Architettura di produzione**: i due servizi, gli URL, chi chiama chi.
2. **Configurazione**: le variabili d'ambiente di ogni servizio (nome, valore o "segreto", a cosa serve). **Mai** il valore dei segreti.
3. **Come si rilascia**: i passi, da `develop` alla produzione.
4. **Come si verifica**: cosa controllano gli smoke test, come si lanciano a mano.
5. **Come si torna indietro (rollback)**: i passi su Render, quanto tempo richiede, cosa fare dopo.
6. **Limiti noti dell'ambiente**: cold start, dati in memoria, ore del piano Free.

## Livello 3: Escalation (facoltativo)

1. **Esercitazione di rollback.** Su un branch sabotate la Bottega in modo che i test della CI restino verdi ma la produzione diventi pericolosa (indizio: c'è un controllo che vale **solo** quando `BOTTEGA_ENV` è `produzione`). Merge su `main`: `test` verde, `deploy` verde, `smoke` **rosso**. Rollback su Render (servizio bottega › **Deploys** › sulla riga del deploy precedente, **Rollback** › **Rollback to this deploy**), cronometrando. Poi `git revert`, PR, merge.
2. **Prova generale (shift-left).** Si poteva scoprire **prima** del deploy? Nel job `test`, accendete una terza istanza della Bottega con `BOTTEGA_ENV=produzione` sulla porta 8002 e lanciateci contro `pytest smoke`. Rifate il sabotaggio: ora si ferma al job `test`.
3. **Due merge in un minuto.** Cercate la chiave `concurrency` di GitHub Actions e usatela sul job `deploy`, in modo che i deploy vadano in fila. Perché `cancel-in-progress: false` e non `true`?

## Documentazione

- Render, deploy hook: https://render.com/docs/deploy-hooks
- Render, deploy e auto-deploy: https://render.com/docs/deploys
- Render, rollback: https://render.com/docs/rollbacks
- Render, piano Free: https://render.com/docs/free
- Render, variabili d'ambiente predefinite (`RENDER_GIT_COMMIT`): https://render.com/docs/environment-variables
- gunicorn, impostazioni: https://gunicorn.org/reference/settings/
- GitHub Actions, secrets: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- GitHub Actions, variables: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables
- GitHub Actions, concurrency: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
- Martin Fowler, Continuous Delivery: https://martinfowler.com/bliki/ContinuousDelivery.html
