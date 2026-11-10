# SETUP RENDER — La Bottega va in produzione

> 📖 Una parola non vi è chiara? Cercatela in [`CONCETTI_BASE.md`](../CONCETTI_BASE.md), il dizionario del corso.

Mercoledì 11/11 la Bottega smette di girare solo sul vostro PC: la mettiamo **online**, su un server vero, raggiungibile da chiunque con un link. Il deploy lo farà la **pipeline**, da sola, solo dopo che i test sono verdi.

Il cloud che usiamo si chiama **Render** (https://render.com). È una PaaS (Platform as a Service): voi date il codice e il comando di avvio, Render pensa a server, rete, HTTPS e dominio. Niente Docker (lo vedete in un altro modulo), niente carta di credito.

> **Questo file ha due parti.**
> - **Parte A: a casa, OBBLIGATORIA, la sera di martedì 10/11** (circa 15 minuti). Senza la Parte A, in aula potete solo guardare: il deploy lo farete a casa.
> - **Parte B: in aula** durante il Lab 3, seguendo la traccia guidata. Chi non finisce in aula la completa a casa (è il Livello 1 del compito).

---

## Cosa offre (e cosa NON offre) il piano Free

| Caratteristica | Piano Free | Cosa vuol dire per noi |
|----------------|------------|------------------------|
| Costo | 0 €, **nessuna carta di credito** | Se vi chiede una carta, fermatevi: avete scelto un piano a pagamento |
| Ore incluse | 750 ore al mese **per workspace** | Bastano per 2 servizi, perché quando dormono non consumano ore |
| Inattività | Dopo **15 minuti** senza richieste il servizio si **addormenta** | La prima richiesta dopo una pausa ci mette **circa un minuto** (cold start) |
| Disco | **Effimero**: si azzera a ogni deploy, riavvio o risveglio | La Bottega tiene i dati in memoria: a ogni risveglio riparte da zero. Per noi va bene |
| Rollback | Sì, ai deploy precedenti più recenti | Lo vedete nella demo del docente |

Il cold start non è un difetto da nascondere: è un **guasto gratuito**. Ricordate il corriere lento? Qui tutti e due i servizi possono essere "lenti" per un minuto.

> ⚠️ **Non usate servizi esterni di "ping" per tenerli svegli.** Due servizi sempre accesi consumano 2 × 720 = 1.440 ore al mese: oltre le 750 ore, Render **sospende tutti i servizi Free** del workspace fino al mese successivo.

---

## Parte A — A casa, la sera del 10/11 (OBBLIGATORIA)

### A1. Il repository è pronto?

Vi serve il repository GitHub **privato** della Bottega, quello che avete consegnato per la G1. Controllate:

- [ ] è su GitHub e ci potete fare push;
- [ ] la radice del repository è la cartella della Bottega (`app.py` deve stare in cima, non dentro una sottocartella);
- [ ] il branch principale si chiama `main`. Se si chiama `master`, rinominatelo: su GitHub andate in **Settings › General › Default branch** e cliccate sull'icona della matita;
- [ ] esiste anche il branch `develop` (Git Flow, semestre 1). Se manca: `git checkout -b develop && git push -u origin develop`.

### A2. Create l'account Render

1. Andate su https://dashboard.render.com/register.
2. Scegliete **GitHub** come metodo di accesso. È il più comodo, perché collega subito i due account.
3. Confermate l'indirizzo email se Render ve lo chiede.
4. Se Render vi chiede come lo userete, scegliete un uso personale o di studio (la voce esatta può cambiare). Il workspace che ottenete è quello gratuito.
5. **Nessuna carta di credito.** Se una schermata la chiede, state cercando di creare qualcosa a pagamento: tornate indietro.

### A3. Autorizzate Render a leggere SOLO il repository della Bottega

Quando Render chiede l'accesso a GitHub (succede la prima volta che create un servizio, oppure da **Account Settings**):

1. scegliete **Only select repositories**;
2. selezionate **soltanto** il repository della Bottega;
3. confermate.

> Perché non "All repositories"? Per il **principio del privilegio minimo**, lo stesso del `.env` del semestre 1: si dà a ogni sistema **solo** l'accesso che gli serve. Se domani l'account Render venisse compromesso, l'attaccante vedrebbe un solo repository, non tutti.

### A4. Verifica

Nella dashboard di Render cliccate **New › Web Service**. Nella lista dei repository Git dovete vedere quello della Bottega. **Non create ancora niente**: fermatevi qui e chiudete la pagina.

✅ La Parte A è finita. Se qualcosa non va, scrivete al docente **martedì sera**, così mercoledì mattina lo sistemiamo nei primi minuti invece che durante il lab.

---

## Parte B — In aula (Lab 3): i due servizi

Creiamo **due** servizi dallo **stesso** repository, come nell'architettura che conoscete:

```
   Internet ──HTTPS──▶  bottega-<nome>.onrender.com  ──HTTPS──▶  corriere-<nome>.onrender.com
                        gunicorn app:app                          gunicorn corriere:app
                        BOTTEGA_ENV=produzione                    (il fornitore "finto")
                        CORRIERE_URL=https://corriere-...
```

### B0. Il repository deve essere pronto per la produzione

Prima di creare i servizi, nel repository devono esserci (chi parte da `bottega_start/` li ha già):

- `requirements.txt` con **solo** le dipendenze di produzione, compreso `gunicorn==26.2.0`;
- `requirements-dev.txt` con `-r requirements.txt` più pytest e gli strumenti di test;
- `.python-version` con dentro `3.14`;
- in `app.py`, `/api/health` che risponde anche con la `versione` (due righe, spiegate nel passo 1 del Lab 3).

Se mancano, copiateli da `testing-day9/bottega_start/`: è il **passo 1** di `lab3_deploy/README.md`. Devono arrivare anche su `main`, perché Render legge `main`: se al passo 1 avete fatto push solo su `develop`, fate una Pull Request `develop` → `main` e il merge **prima** di creare i servizi.

### B1. Il servizio del corriere (lo creiamo per primo)

1. Dashboard › **New › Web Service** › selezionate il repository della Bottega.
2. Compilate così:

   | Campo | Valore |
   |-------|--------|
   | Name | `corriere-<vostronome>` (es. `corriere-mario-rossi`) |
   | Region | **Frankfurt (EU Central)**, la più vicina all'Italia |
   | Branch | `main` |
   | Root Directory | vuoto (lasciatelo vuoto se `app.py` è nella radice del repo) |
   | Language / Runtime | **Python 3** |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn corriere:app` (**attenzione**: Render riconosce Flask e precompila `gunicorn app:app`, che qui è sbagliato: cambiatelo) |
   | Instance Type | **Free** (`$0 / month`) |

   Prima di creare il servizio aprite la sezione **Advanced** in fondo alla pagina: **Health Check Path** lasciatelo **vuoto** (il corriere non ha un endpoint di health) e **Auto-Deploy** mettetelo su **Off**. Il corriere "non è nostro": non deve ripartire a ogni nostro push.

3. Cliccate **Deploy Web Service** e guardate i log: dovete vedere l'installazione dei pacchetti e poi una riga di gunicorn con `Listening at: http://0.0.0.0:10000`.
4. Copiate l'URL del servizio (in alto, `https://corriere-....onrender.com`) e provatelo nel browser aggiungendo `/tariffa?cap=50100&peso=1`. Risultato atteso: `{"costo":4.9}`. (Se aprite solo l'indirizzo senza `/tariffa...` vedete "Not Found": è normale, il corriere non ha una pagina iniziale.)

### B2. Il servizio della Bottega

1. Dashboard › **New › Web Service** › stesso repository.
2. Compilate come prima, ma con:

   | Campo | Valore |
   |-------|--------|
   | Name | `bottega-<vostronome>` |
   | Start Command | `gunicorn app:app` |
   | Instance Type | **Free** |

3. **Environment Variables** (nella stessa pagina, oppure dopo, da **Environment**):

   | Key | Value |
   |-----|-------|
   | `BOTTEGA_ENV` | `produzione` |
   | `CORRIERE_URL` | l'URL del corriere del punto B1, **senza** `/` finale (es. `https://corriere-mario-rossi.onrender.com`) |

4. **Advanced** (in fondo alla pagina, prima di creare il servizio):
   - **Health Check Path**: `/api/health`. Render non manda traffico alla nuova versione finché questo endpoint non risponde 2xx.
   - **Auto-Deploy**: **Off**. Da adesso deploya **solo la pipeline**, e solo dopo i test (Lab 3, passo 4).
5. **Deploy Web Service**. Quando il deploy è finito (circa un minuto), aprite `https://bottega-<vostronome>.onrender.com/api/health`. Risultato atteso: `"ambiente":"produzione"`.

   Vi siete dimenticati l'Auto-Deploy? Si cambia anche dopo, dalle **Settings** del servizio.

> Perché `gunicorn app:app` e non `python app.py`? `python app.py` avvia il server di **sviluppo** di Flask, che serve una richiesta per volta e non è fatto per Internet. `gunicorn` è un server di produzione. Il primo `app` è il file `app.py`, il secondo è la variabile `app = Flask(...)` dentro il file. Non serve indicare la porta: Render la scrive nella variabile d'ambiente `PORT` (di default 10000) e gunicorn la legge da solo.

### B3. Il deploy hook diventa un segreto di GitHub

Il **deploy hook** è un URL che, se chiamato, fa partire un deploy. Chiunque lo conosca può deployare la vostra app: **è una password**.

1. Su Render, servizio **bottega** › **Settings** › sezione **Deploy Hook** › copiate l'URL (`https://api.render.com/deploy/srv-...?key=...`).
2. Su GitHub, nel repository: **Settings › Secrets and variables › Actions**.
3. Tab **Secrets** › **New repository secret**:
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Secret: l'URL appena copiato

   > ⚠️ Copiate l'URL da Render e incollatelo **subito** nel campo del secret, senza copiare nient'altro in mezzo. Se negli appunti finisce altro (un comando, uno spazio, un a capo), nel secret va il valore sbagliato e la pipeline si ferma con un errore sul formato dell'URL.
4. Tab **Variables** › **New repository variable**, due volte:
   - `PRODUZIONE_URL` = `https://bottega-<vostronome>.onrender.com`
   - `CORRIERE_URL` = `https://corriere-<vostronome>.onrender.com`

> Secret o Variable? Gli URL pubblici sono **variabili**: non sono segreti, li vede chiunque apra il sito. Il deploy hook è un **secret**: GitHub lo cifra, lo nasconde nei log (`***`) e non lo mostra più a nessuno, nemmeno a voi. È lo stesso principio del `.env` del semestre 1, ma lato pipeline.
>
> Se il deploy hook finisce per sbaglio in un commit, in una chat o in uno screenshot: Render › Settings › **Regenerate Hook**, poi aggiornate il secret su GitHub. Il vecchio URL smette subito di funzionare (risponde 401).

---

## Problemi frequenti

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| Il repository non compare nella lista | Render non ha accesso a quel repository | Account Settings › GitHub › **Configure** › aggiungete il repository |
| Build fallita: `Could not open requirements file` | `requirements.txt` non è nella radice | Controllate la **Root Directory** (vuota, oppure il nome della sottocartella) |
| Build fallita: versione di Python | `.python-version` scritto male | Una sola riga: `3.14` |
| Log: `ModuleNotFoundError: No module named 'gunicorn'` | gunicorn manca in `requirements.txt` | Aggiungete `gunicorn==26.2.0` e fate push |
| La CI è rossa con `No module named 'playwright'` | Avete i test del browser in `tests/e2e/` | Nello step dei test: `pytest -v --ignore=tests/e2e` (come in `bottega_start/`) |
| `/api/health` dice `"ambiente":"sviluppo"` | Manca `BOTTEGA_ENV` | Environment › aggiungete `BOTTEGA_ENV=produzione` (Render rideploya) |
| Il primo checkout online risponde **503** | Il corriere stava dormendo: mentre si sveglia non risponde come dovrebbe, e la Bottega lo traduce in 503 | È il comportamento **corretto** (contratto della Bottega). Riprovate dopo un minuto |
| La pagina ci mette un minuto ad aprirsi | Cold start del piano Free | Normale: il servizio si stava risvegliando |
| Il carrello si è svuotato da solo | Il servizio si è addormentato e i dati erano in memoria | Normale per noi: disco e memoria sono effimeri |

## Documentazione

- Render, piano Free: https://render.com/docs/free
- Render, Flask: https://render.com/docs/deploy-flask
- Render, web service e porta: https://render.com/docs/web-services
- Render, variabili d'ambiente: https://render.com/docs/configure-environment-variables
- Render, deploy hook: https://render.com/docs/deploy-hooks
- Render, versione di Python: https://render.com/docs/python-version
- GitHub, secrets: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
