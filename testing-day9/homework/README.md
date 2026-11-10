# Homework: il primo rilascio, e la pagina per chi decide

## Contesto

Oggi avete visto la Bottega andare in produzione da sola, con la pipeline, e i report dei test scritti per lettori diversi. Il compito chiede una cosa sola, ma fatta bene: spiegare a chi deve decidere **se la Bottega si può rilasciare**, con i numeri veri dei vostri test. Il deploy sul vostro repository è facoltativo.

**Il Livello 1 è obbligatorio** e richiede circa un'ora e mezza. I Livelli 2 e 3 sono **facoltativi**.

> 🧩 **Prima di iniziare:** rileggete [`sommario_lezione_9.md`](../sommario_lezione_9.md). Se vi bloccate, scrivete nel `README.md` del repository **dove** vi siete bloccati e **cosa** avete provato: conta anche quello.

## Livello 1: Sopravvivenza (obbligatorio per tutti)

### 1. I numeri (circa 15 minuti)

Con corriere e app accesi, nel vostro repository, copiate [`test_difetti_noti.py`](../lab2_reporting/test_difetti_noti.py) in `tests/` e lanciate:

```bash
pytest -rxXs
pytest --html=report/report.html --self-contained-html
```

Contate passati, falliti, difetti noti (`x`) e saltati (`s`): sono i numeri della sezione 4 del Test Report. Il resto è nel [Lab 2, Livello 1](../lab2_reporting/README.md).

### 2. Il Test Report di una pagina (circa 1 ora)

Create `TEST_REPORT.md` nella radice del repository, partendo da [`TEMPLATE_TEST_REPORT.md`](TEMPLATE_TEST_REPORT.md). I dati dell'azienda sono in [`DOSSIER_CTO.md`](DOSSIER_CTO.md): leggetelo prima.

- I numeri dei test sono quelli **veri** del punto 1 (passati, falliti, difetti noti, saltati). Se avete fatto anche il deploy, potete usare la vostra ultima run su `main`, con il link.
- La sezione 7 contiene i **costi e i benefici** di almeno un intervento del dossier (il refactoring di `preventivo.py` oppure la protezione dal corriere lento): quanto costa, quanto costa **non** farlo al mese, in quanti mesi si ripaga. Con le ipotesi scritte.
- **Una pagina**, niente gergo, una raccomandazione (GO / GO condizionato / NO-GO) motivata, e almeno una **decisione richiesta** alla CTO (per esempio DEC-001, che non spetta a voi).

> 🧩 **Non sai da dove partire?** Rileggete il report ad alta voce, come se lo leggeste alla CTO al telefono. Ogni parola che lei non capirebbe (fixture, mock, xfail, 500, endpoint, pipeline...) va riscritta come la direbbe un cliente: "il sito va in errore", "difetto noto e registrato".

Come lo valuto:

| Criterio | Cosa guardo |
|----------|-------------|
| Una pagina | tutte le sezioni del template, niente elenchi di nomi di test |
| Numeri | i risultati veri dei vostri test; costo, "non fare niente" al mese e break-even, con le ipotesi |
| Linguaggio | si capisce senza sapere cos'è un test; i difetti sono descritti con l'effetto sul cliente o sull'azienda |
| Raccomandazione | motivata, con le condizioni (se GO condizionato) e una decisione richiesta con una scadenza |

## Livello 2: Ingegneria (facoltativo, scegliete quello che volete)

1. **Il deploy della vostra Bottega** (circa 2 ore). Prima la **Parte A** di [`SETUP_RENDER.md`](../SETUP_RENDER.md), poi la traccia di [`lab3_deploy/README.md`](../lab3_deploy/README.md), Livello 1, passi 1-5. È fatto quando:
   - [ ] su `main` la pipeline esegue `test` → `deploy`, entrambi **verdi**;
   - [ ] `https://bottega-<nome>.onrender.com/api/health` risponde con `"ambiente":"produzione"` e con la `versione` uguale ai primi 7 caratteri del vostro ultimo commit su `main`;
   - [ ] `POST /api/reset` sulla vostra produzione risponde **403**;
   - [ ] l'**Auto-Deploy** di Render è **Off** su entrambi i servizi.

   ⚠️ **Vietato** scrivere il deploy hook nel codice, nel workflow o in un file del repository: va solo nei **Secrets** di GitHub. Se lo trovo, il Livello 2 non vale e dovete rigenerare l'hook su Render.
2. **I report nella pipeline.** Il job `test` produce `report.html` e `junit.xml` e li carica come artifact `report-test` ([`lab2_reporting/README.md`](../lab2_reporting/README.md), Livello 2). Nel Test Report, alla riga "Report tecnici completi", mettete il link alla run con l'artifact.
3. **Il codice di Gianni.** [`lab1_legacy/README.md`](../lab1_legacy/README.md), Livello 2: la gabbia, tre passi di refactoring con un commit ciascuno, il ticket BOT-42 corretto con il test scritto prima. Su un branch `legacy`.

## Livello 3: Escalation (facoltativo)

1. **Smoke test in produzione** ([`lab3_deploy/README.md`](../lab3_deploy/README.md), Livello 2): la cartella `smoke/` e il job `smoke` dopo il `deploy`, che aspetta la versione giusta e controlla almeno ambiente di produzione, reset vietato (403), nessun `Traceback`, errori in JSON. Vietato fare ordini o chiamare `/api/reset` con successo: la produzione non si sporca. Ogni chiamata di rete ha un `timeout`.
2. **Il runbook**: `RILASCIO.md` con le 6 sezioni del Lab 3, Livello 2, punto 4. Nessun segreto dentro.
3. **Il codice di Gianni, Livello 3**: la funzione estratta e la richiesta CR-07 in TDD.
4. **Esercitazione di rollback** (Lab 3, Livello 3, punto 1), documentata in fondo a `RILASCIO.md`: cosa avete sabotato, il link alla run con lo smoke rosso, quanto è durato il rollback.

---

## Istruzioni per la consegna

1. Lavorate sul repository **privato** che usate dalla G1 (il docente è già collaboratore).
2. Mandate a `angeligiovanni21@gmail.com`, entro le **23:59 di domenica 22 novembre 2026**:
   - il link del repository (con `TEST_REPORT.md` nella radice);
   - se avete fatto il Livello 2 o 3, una riga che dice quali punti; per il deploy, l'URL della vostra Bottega su Render e il link all'ultima run **verde** su `main`.

> Bloccati? Scrivetemi **prima** di domenica, con lo screenshot dell'errore. Non la domenica sera alle 23.
