# LAB 2 — GAME DAY: squadra rossa contro squadra blu

> 📖 **Parole da sapere per questo lab** (spiegate con esempi in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [Chaos Engineering](../../CONCETTI_BASE.md#chaos-engineering) · [latenza](../../CONCETTI_BASE.md#latenza) · [media e percentile](../../CONCETTI_BASE.md#media-e-percentile)

## Contesto

Le grandi aziende organizzano dei **Game Day**: giornate in cui un gruppo rompe **apposta** un sistema e un altro gruppo, senza sapere cosa è stato rotto, deve accorgersene, capire cosa succede e reagire. È un'esercitazione antincendio per il software: quando l'incendio vero arriva (di notte, il giorno di Black Friday), le persone sanno già cosa fare.

Oggi lo facciamo noi, sulla Bottega.

- **Squadra rossa: il docente.** Durante la pausa passa sul "server di produzione" di ogni squadra e, forse, rompe qualcosa. Ogni squadra ha un guasto **diverso**: guardare il PC dei vicini non serve.
- **Squadra blu: voi.** Al rientro dovete **rilevare** il guasto (con una prova!) e **diagnosticarlo** entro **12 minuti**, usando solo gli strumenti di un vero turno di reperibilità.

Gli incidenti veri arrivano così: mentre non c'eri. Oggi si gioca **un round**; se avanza tempo, il docente ne fa giocare un secondo.

## Prima della pausa: il server di produzione

Squadre da 4-5 persone, decise dal docente. Ogni squadra sceglie **un PC**, che da adesso è il suo "server di produzione": `bottega_g5` con corriere (terminale 1) e app (terminale 2) accesi, nessun guasto attivo.

1. Il corriere deve essere quello **sano** (dopo il Lab 1: terminale 1 CTRL+C e `python chaos_ctl.py corriere`, senza opzioni).
2. Terminale 3: `python misura.py` → `VERIFICATA`.
3. Lasciate il PC **acceso**, con i tre terminali aperti, e andate in pausa. Se il PC si blocca da solo dopo qualche minuto, ditelo al docente **prima** di uscire.

## Le squadre e i ruoli

Nella squadra ognuno ha un ruolo, come in un incidente vero:

| Ruolo | Cosa fa |
|-------|---------|
| **Incident Commander (IC)** | decide cosa si prova e in che ordine, e consegna la diagnosi al docente. **Non** tocca la tastiera |
| **Operatore** | l'unico che usa la tastiera del server di produzione |
| **Scriba** | sul **suo** portatile tiene il file `INCIDENTE.md`: ora, cosa è stato fatto, cosa si è visto |
| **Comunicazioni** | ogni 4 minuti detta allo Scriba un aggiornamento di 1 riga "per i clienti" (es. "Stiamo indagando su rallentamenti nel pagamento") |

Con 4 persone, lo Scriba fa anche le Comunicazioni.

## Il file `INCIDENTE.md`

Niente fogli: tutto quello che scoprite va in un file. Lo Scriba lo crea sul suo portatile e ci copia questa traccia:

> 🧩 **Traccia di `INCIDENTE.md`** (lo Scriba sostituisce i `???` mentre si indaga):
>
> ```markdown
> # Incidente · squadra ???
> IC: ???   Operatore: ???   Scriba: ???   Comunicazioni: ???
> Inizio indagine: ???
>
> ## Timeline
> | Ora | Cosa abbiamo fatto / visto | Fonte (misura.py / pytest / browser / curl / log) |
> |-----|----------------------------|---------------------------------------------------|
> | ??? | ??? | ??? |
>
> ## Aggiornamenti per i clienti (ogni 4 minuti)
> - ??? : ???
>
> ## RILEVATO alle ???
> Prova (comando + numero): ???
>
> ## DIAGNOSI alle ???
> - Componente: corriere / Bottega, endpoint ??? / nessun guasto
> - Tipo: lento / errori intermittenti (~???%) / morto / comportamento sbagliato / nessun guasto
> - Impatto sul cliente (una frase senza gergo): ???
> - Mitigazione proposta: ???
> - Ticket del cliente chiesto? no / sì, alle ???
> - Punti: ???
> ```

A fine gioco lo Scriba **manda il file a tutta la squadra**: vi serve per il postmortem del compito.

## Come si svolge il round (20 minuti)

**1. Indagine (12').** Al via del docente parte il cronometro. Quando avete una **prova** concreta che qualcosa non va (un numero, un test rosso, un messaggio di errore), l'IC dice ad alta voce «**RILEVATO**» e lo Scriba annota l'ora e la prova. Poi continuate fino alla **diagnosi**: quale componente, che tipo di guasto, che impatto sul cliente, che mitigazione proponete. Quando la diagnosi è scritta in `INCIDENTE.md`, l'IC chiama il docente e la legge: si consegna **una volta sola**.

> Dopo 6 minuti senza aver rilevato niente, potete chiedere al docente il **ticket del cliente**: vi legge la segnalazione di un cliente. È gratis: in un turno vero le segnalazioni dei clienti si leggono sempre.

**2. Rivelazione (5').** Il docente vi dice cosa aveva rotto e scrive i punti alla lavagna. Lo Scriba copia i punti in `INCIDENTE.md`.

**3. Ripristino (3').** Terminale 1 CTRL+C e `python chaos_ctl.py corriere`, terminale 3 `python chaos_ctl.py stop`, poi `python misura.py` → `VERIFICATA`.

## Cosa può usare la squadra blu (e cosa no)

| ✅ Permesso — quello che avreste in un turno vero | ❌ Vietato (−3 punti) |
|-----------------------------------------------------|------------------------|
| Browser e DevTools (scheda Network!) | Guardare o toccare il **terminale 1**: il corriere è il server di **un'altra azienda**, non avete accesso |
| `pytest`, `python misura.py`, `curl` | `chaos_ctl.py`, in qualsiasi forma, e `/api/chaos` |
| Leggere i **log** di `app.py` nel terminale 2: sono i **vostri** log | **Riavviare `app.py`**: cancellereste le prove (e nella realtà, spesso, nemmeno risolve) |
| Leggere il codice (`app.py`, `spedizioni.py`, ...) | **Modificare** un file `.py`: l'app si riavvierebbe da sola (vedi sopra) |
| Chiamare direttamente l'**API pubblica** del corriere: `curl "localhost:8001/tariffa?cap=50100&peso=1"` | La cronologia dei comandi (freccia su nel terminale 3: ci sono i comandi del docente) |

## Punteggio

| Voce | Punti |
|------|-------|
| Guasto **rilevato** con una prova concreta entro 12' | +2 |
| **Diagnosi corretta** (componente + tipo) · parziale (solo componente, o solo il sintomo) | +3 · +1 |
| "Nessun guasto", se è davvero così, dichiarato con le prove | +5 |
| Mitigazione proposta sensata | +1 |
| Infrazione delle regole | −3 |

Attenzione: **non è detto che tutte le produzioni siano rotte**. Chi dichiara un guasto che non esiste non prende i punti della diagnosi. Il vostro avversario non è il docente: è la tentazione di vedere quello che vi aspettate di vedere.

## Consigli da reperibile (leggeteli PRIMA di iniziare)

1. **Partite dalla misura.** Prima ancora di pensare: `python misura.py`. Avete i numeri di "sano" del Lab 1: confrontate.
2. **Dal sintomo al componente.** Un 503 con `"servizio spedizioni non disponibile"` dice una cosa; un 502 in HTML ne dice un'altra; un 400 "carrello vuoto" potrebbe essere l'effetto di un guasto **da un'altra parte**.
3. **Isolate.** Il corriere risponde se lo chiamate direttamente? Il problema è su tutti gli endpoint o su uno solo? Su tutte le richieste o su alcune?
4. **Una misura non è una prova.** Un test che passa una volta non dimostra niente se il guasto è intermittente: ripetete, o usate `misura.py` con più richieste.
5. **Scrivete tutto con l'ora** in `INCIDENTE.md`. La timeline vi servirà subito dopo, nel postmortem (e nel compito).

> 🧩 **Non sai da dove partire?** Ecco la checklist della squadra blu, nell'ordine in cui conviene seguirla. L'IC la legge ad alta voce, l'Operatore esegue, lo Scriba copia i `???` in `INCIDENTE.md`:
>
> ```text
> [ ] 1. python misura.py                     → endpoint fuori soglia: ???   errori ???%   p95 ???s
>                                               (confronto con i numeri "sani" del Lab 1)
> [ ] 2. pytest                               → test rossi: ???
>        Se 1 o 2 mostrano qualcosa: l'IC dice «RILEVATO» alle ??? con la prova: ???
> [ ] 3. Status code che vede il cliente      → 400 / 500 / 502 / 503 / nessuno: ???
>        (misura.py, colonna status · oppure DevTools, scheda Network)
> [ ] 4. Il corpo della risposta è JSON o HTML? → ???
> [ ] 5. curl "localhost:8001/tariffa?cap=50100&peso=1"   → il corriere risponde? ???   in quanti secondi? ???
> [ ] 6. curl localhost:8000/api/health       → ???
> [ ] 7. Log di app.py (terminale 2)          → righe strane: ???
> [ ] 8. Il guasto è su tutte le richieste o su alcune?  python misura.py --checkout 50 → ???%
> [ ] 9. Un acquisto a mano nel browser, come un cliente: prezzi e totale tornano? ???
> [ ] 10. Tutto dentro le soglie e tutto giusto a mano? Allora la diagnosi può essere "nessun guasto". Prove: ???
>
> DIAGNOSI   componente: ???   tipo: lento / errori intermittenti / morto / comportamento sbagliato / nessun guasto
>            impatto sul cliente (una frase senza gergo): ???
>            mitigazione: ???
> ```
>
> **Trucco:** un sintomo sul checkout non vuol dire che il guasto sia nel checkout. Prima di scrivere il componente, controllate i passi 5 e 6: dicono se il problema è nostro o del corriere.

## Dopo il gioco: il postmortem (a voce)

Alla fine ogni squadra racconta in due frasi l'incidente che ha **subìto**: qual è stata la prima prova concreta, con quale comando, e cosa avrebbe aiutato ad accorgersene prima. Regola d'oro: è **blameless**. Si dice cosa è successo e perché il **sistema** lo ha permesso, non chi ha sbagliato.

La versione scritta, corta, è nel compito: `POSTMORTEM_TEMPLATE.md` in questa cartella, partendo da `INCIDENTE.md`.

## Documentazione

- Google SRE Book, *Managing Incidents* (i ruoli: Incident Commander, Operations, Communications): https://sre.google/sre-book/managing-incidents/
- Google SRE Book, *Postmortem Culture: Learning from Failure*: https://sre.google/sre-book/postmortem-culture/
- Principles of Chaos Engineering: https://principlesofchaos.org/
- Chrome DevTools, scheda Network: https://developer.chrome.com/docs/devtools/network
