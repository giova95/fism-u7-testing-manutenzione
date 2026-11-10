# LAB 1 — Il codice di Gianni (compito facoltativo)

> 📖 **Parole da sapere per questo lab** (spiegate con esempi in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [codice legacy](../../CONCETTI_BASE.md#codice-legacy) · [refactoring](../../CONCETTI_BASE.md#refactoring) · [bug di regressione](../../CONCETTI_BASE.md#bug-di-regressione) · [debito tecnico](../../CONCETTI_BASE.md#debito-tecnico) · [mock](../../CONCETTI_BASE.md#mock)

> **Come si usa questo lab.** In aula lo avete visto fare dal docente, in mezz'ora. Qui lo rifate voi, con calma, sul vostro repository. È un compito **facoltativo**: Livello 2 e 3 del compito (`homework/README.md`). Prima finite il deploy e il Test Report.

## Contesto

`preventivo.py` calcola il totale di ogni ordine della Bottega. L'ha scritto Gianni nel 2019, poi l'hanno "ritoccato" in due. Gianni se n'è andato. Non ci sono test, non c'è documentazione, e l'unico commento utile dice `NON TOCCARE funziona!!!`. Intanto il servizio clienti ha aperto un ticket.

L'ordine dei lavori, quello che avete visto in aula:

| Passo | Cosa | Perché in quest'ordine |
|-------|------|------------------------|
| 1. **Gabbia** | si fotografa cosa fa il codice **oggi**, bug compresi | senza fotografia non sapete se una modifica ha rotto qualcosa |
| 2. **Refactoring** | si cambia la **forma**, a piccoli passi, con la gabbia sempre verde | codice leggibile = modifiche più veloci e meno rischiose |
| 3. **Modifica** | si corregge il bug, con il test scritto **prima** | il test dimostra il bug, poi dimostra la correzione, poi resta per sempre |

| Test "normale" | Characterization test (la gabbia) |
|----------------|-----------------------------------|
| parte dalla **specifica** | parte dal **codice** |
| "il totale **deve** essere 79,90" | "il totale **oggi è** 79,90" |
| rosso = il codice è sbagliato | rosso = il codice è **cambiato** |

## Prima di iniziare (10 minuti)

1. Lavorate sul vostro repository, su un branch nuovo: `git checkout develop && git checkout -b legacy`. Prima di toccare qualcosa, `git status` deve dire *working tree clean*: oggi si fa **un commit per ogni passo**, e il commit è la rete di sicurezza.
2. `preventivo.py` deve essere quello originale, con i `print("DEBUG ...")`. Se l'avete modificato, prendete quello di `testing-day9/bottega_start/`.
3. I test di oggi **non** hanno bisogno del server: testano una funzione. Vanno in una cartella separata, con il suo `conftest.py`, così non ereditano la fixture `stato_pulito` di `tests/` (che vuole il server acceso):

   ```bash
   mkdir tests_preventivo
   pytest tests_preventivo          # si lancia sempre così, server spenti
   ```

4. Verifica veloce, dalla radice del repository:

   ```bash
   python -c "import preventivo; print(preventivo.calcola_totale([{'prezzo': 10, 'quantita': 1}], 'nuovo', '', '50100', 4.9))"
   ```

   Dovete vedere due righe `DEBUG` e poi `14.9`. (Su Windows, se le virgolette danno problemi, aprite `python` e scrivete le due istruzioni una per riga.)

## Livello 2: la gabbia, tre passi di refactoring, il ticket (facoltativo, circa 2 ore)

### 1. La tecnica di Feathers: lasciate che sia il test a dirvi la risposta

Create `tests_preventivo/test_preventivo_caratterizzazione.py`:

```python
from preventivo import calcola_totale

MOUSE = [{"prezzo": 34.5, "quantita": 1}]
TASTIERA = [{"prezzo": 89.9, "quantita": 1}]


def test_cliente_nuovo_senza_codice():
    assert calcola_totale(MOUSE, "nuovo", "", "50100", 4.9) == 0    # <- 0 messo APPOSTA
```

Lanciatelo: è rosso, e il messaggio vi dice il valore vero (`assert 39.4 == 0`). **Copiatelo nel test** al posto dello `0`. Avete fotografato un comportamento.

> Non fate i conti a mano per "verificare" che 39,40 sia giusto. **Oggi** il codice dice 39,40, e domani deve dire lo stesso.

Poi fotografate altri cinque comportamenti, un test ciascuno, con lo stesso metodo:

1. un cliente VIP con più di 100 € di spesa (due tastiere);
2. un ordine sopra i 49,99 € a Firenze (`50100`): quanto costa la spedizione?
3. un ordine sotto i 49,99 € spedito in Sardegna (CAP `09100`);
4. lo **stesso** ordine sopra i 49,99 € del punto 2, ma spedito in Sardegna: la maggiorazione per le isole c'è ancora?
5. due clienti nuovi, uno dopo l'altro, con lo stesso carrello e il codice `BENVENUTO10`: pagano uguale?

Quando un comportamento vi sembra **strano**, non correggetelo. Chiamate il test `test_documenta_...` e scrivete nel commento la domanda da fare al cliente. Decidere se è un bug non spetta a voi.

> 🧩 **Non sai da dove partire?** Lo scheletro dei punti 1, 3, 4 e 5. Sostituite i `???`, lanciate, copiate il valore vero al posto dello `0`:
>
> ```python
> def test_vip_sopra_100_euro_ha_il_15_per_cento():
>     due_tastiere = [{"prezzo": 89.9, "quantita": ???}]          # 179,80 €: sopra i 100
>     #                    righe         tipo   codice  CAP      spedizione
>     assert calcola_totale(due_tastiere, "???", "",    "50100", 9.9) == 0
>
> def test_isole_maggiorazione_di_5_euro_sotto_soglia():
>     assert calcola_totale(MOUSE, "nuovo", "", "???", 4.9) == 0         # CAP di Cagliari
>
> def test_documenta_isole_maggiorazione_sparisce_sopra_soglia():
>     # Bug o scelta? Non lo decidiamo noi: domanda per il cliente
>     assert calcola_totale(???, "nuovo", "", "09100", 9.9) == 0
>
> def test_documenta_benvenuto10_vale_una_sola_volta_per_tutto_il_processo():
>     primo = calcola_totale(TASTIERA, "nuovo", "BENVENUTO10", "50100", 9.9)
>     secondo = calcola_totale(TASTIERA, "nuovo", "???", "50100", 9.9)
>     assert (primo, secondo) == (0, 0)                                  # <- tutti e due APPOSTA
> ```
>
> L'ordine dei parametri è nella prima riga di `calcola_totale`, in `preventivo.py`.

Ora copiate in `tests_preventivo/` il file `starter/conftest.py` di questo lab e leggete la fixture `sconti_puliti`. La lista `SCONTI_USATI` è **globale**: se un altro test usasse `BENVENUTO10` prima del vostro `test_documenta_benvenuto10_...`, il "primo" cliente non avrebbe più lo sconto e il test cambierebbe esito in base all'ordine. È la stessa malattia che la `stato_pulito` cura in `tests/`, e la cura è la stessa: si riparte da uno stato pulito prima di ogni test. Lanciate `pytest tests_preventivo`: deve essere verde.

```bash
git add tests_preventivo && git commit -m "test: characterization test di preventivo.py"
```

### 2. Il golden master: migliaia di casi, scritti dal computer

Quante combinazioni di carrello, tipo di cliente, codice, CAP e data ci sono? Migliaia. Nessuno le scrive a mano. L'idea del **golden master**: si **generano** tantissimi input, si esegue il codice su tutti e si **salva** l'output in un file "approvato"; il test riesegue tutto e **confronta**.

Copiate in `tests_preventivo/` gli altri due file dello starter, `golden_master.py` e `test_preventivo_golden_master.py`, e leggete `esegui_caso()`. Combatte tre nemici:

| Nemico | Sintomo | Arma (già scritta) |
|--------|---------|--------------------|
| **il tempo** | `BLACKFRIDAY` dipende da `datetime.date.today()`: un test scritto oggi cambia esito il 24 novembre | `patch("preventivo.datetime")`: si sostituisce il nome **dove viene usato**, come per `spedizioni.requests.get` |
| **lo stato globale** | `BENVENUTO10` funziona solo per il primo caso | `SCONTI_USATI.clear()` prima di ogni caso |
| **i `print`** | migliaia di righe `DEBUG` nel terminale | `redirect_stdout`: decidiamo **noi** che i `print` non fanno parte del comportamento |

Completate l'unico `TODO`, la lista `DATE`: ci vogliono i **bordi** della finestra del Black Friday che trovate in `preventivo.py` (cercate `oggi.day >=` e `oggi.day <=`). Due valori sul bordo valgono più di cento valori a caso.

> 🧩 ```python
> DATE = ["2026-11-23", "2026-11-???", "2026-11-???", "2026-12-25"]
> #        il giorno prima   il primo        l'ultimo       25, ma a dicembre
> ```

Poi:

```bash
python -m tests_preventivo.golden_master     # quanti casi? stampa i primi 5
pytest tests_preventivo --approva            # la PRIMA volta: fotografa e salva il JSON
pytest tests_preventivo                      # da ora in poi: confronta
```

Aprite `tests_preventivo/approvato_preventivo.json`: un caso per riga, ognuno con il suo `"totale"`. Così `git diff` mostrerà **esattamente** quali casi cambiano.

**La gabbia è una gabbia vera?** Cambiate apposta `0.15` in `0.16` in `preventivo.py` e lanciate `pytest tests_preventivo`: il golden master deve diventare rosso e dirvi **quanti** casi sono cambiati. Poi tornate indietro: `git restore preventivo.py`.

```bash
git add tests_preventivo && git commit -m "test: golden master di preventivo.calcola_totale"
```

### 3. Tre passi di refactoring

> **Refactoring** (Martin Fowler): una modifica alla struttura interna del codice che lo rende più facile da capire e da modificare, **senza cambiarne il comportamento osservabile**.

Le regole:
1. **un passo alla volta**, poi `pytest tests_preventivo`;
2. **verde** → commit; **rosso** → `git restore preventivo.py` e si riprova più piccolo. Niente debug: si torna indietro;
3. **i test non si toccano**, e **i bug restano** (un refactoring che corregge un bug non è un refactoring: il golden master ve lo dirà);
4. la firma di `calcola_totale` non cambia (la chiama `app.py`), e non rinominate `SCONTI_USATI` né `import datetime`: la gabbia li usa.

| Passo | Cosa fate | Commit |
|-------|-----------|--------|
| 1 | via i due `print("DEBUG ...")` | `refactor: rimuovi print di debug` |
| 2 | nomi parlanti: `r`→`righe`, `t`→`tipo_cliente`, `c`→`codice`, `sped`→`spedizione`, `tot`→`totale`, `x`→`riga`. Via il commento che spiegava le lettere | `refactor: nomi parlanti` |
| 3 | costanti con un nome in cima al modulo: `SOGLIA_VIP_ALTO = 100`, `SCONTO_VIP_ALTO = 0.15`, `BUONO_BENVENUTO = 10`, `MAGGIORAZIONE_ISOLE = 5`, `SOGLIA_SPEDIZIONE_GRATUITA = 49.99`... | `refactor: costanti al posto dei numeri magici` |

> 🧩 **Passo 3**, lo scheletro delle prime costanti (sotto `import datetime`). I numeri sono quelli che trovate **nel codice**, non quelli che vi sembrano giusti:
>
> ```python
> SOGLIA_VIP_ALTO = ???             # sopra questa cifra il VIP ha lo sconto pieno
> SCONTO_VIP_ALTO = ???
> SCONTO_VIP_BASE = ???
>
> # ... più in basso, dentro calcola_totale:
>     if tipo_cliente == "vip":
>         if totale > SOGLIA_VIP_ALTO:
>             totale = totale - totale * SCONTO_VIP_ALTO
>         else:
>             totale = totale - totale * ???
> ```

**La trappola del float (l'avete vista in aula).** "Togliere il 15%" o "moltiplicare per 0,85" in matematica è la stessa cosa. Provate a sostituire `totale - totale * SCONTO_VIP_ALTO` con `totale * (1 - SCONTO_VIP_ALTO)` e lanciate la gabbia: quanti casi cambiano, e di quanto? Poi tornate indietro. La gabbia non conosce la matematica, conosce il comportamento.

### 4. Il ticket BOT-42, in TDD (manutenzione correttiva)

> **🎫 Ticket BOT-42** · *servizio clienti, priorità Alta*
> "Il codice BENVENUTO10 funziona per il primo cliente nuovo della giornata. Dal secondo in poi il totale non cambia. Il tecnico dice che, se si riavvia il server, torna a funzionare."

**RED.** Create `tests_preventivo/test_ticket_bot42.py` (il numero del ticket nel nome del file: tra un anno qualcuno si chiederà perché esiste quel test):

```python
from preventivo import calcola_totale

TASTIERA = [{"prezzo": 89.9, "quantita": 1}]


def test_bot42_benvenuto10_vale_per_ogni_cliente_nuovo():
    primo_cliente = calcola_totale(TASTIERA, "nuovo", "BENVENUTO10", "50100", 9.9)
    secondo_cliente = calcola_totale(TASTIERA, "nuovo", "BENVENUTO10", "50100", 9.9)
    assert primo_cliente == 79.9
    assert secondo_cliente == 79.9
```

Deve essere **rosso** (`assert 89.9 == 79.9`). Se è verde, non avete riprodotto il bug, e qualsiasi correzione sarebbe una scommessa.

**GREEN.** La causa è la lista globale `SCONTI_USATI`. Toglietela: `calcola_totale` diventa una **funzione pura** (stesso input, stesso output, nessuna memoria). Nel ramo del cliente `"nuovo"` restano solo il controllo sul codice e la sottrazione del buono; poi cancellate anche `SCONTI_USATI = []` in cima al file.

**La gabbia protesta: leggete cosa dice.**
1. Tutti i test in `ERROR`, con `AttributeError: ... has no attribute 'SCONTI_USATI'`: viene dalla fixture `sconti_puliti`, che pulisce una lista che non esiste più. Cancellate la fixture e la riga `preventivo.SCONTI_USATI.clear()` in `esegui_caso()`. Meno stato, meno fixture.
2. `test_documenta_benvenuto10_...` è rosso: fotografava il bug. Cancellatelo, **consapevolmente**, nello stesso commit della correzione: adesso c'è il test del ticket, che dice il contrario.
3. Il golden master è **verde**. Perché non si è accorto di niente? (Rileggete `esegui_caso()`: cosa faceva prima di **ogni** caso?)

```bash
git add -A
git commit -m "fix: BENVENUTO10 vale per ogni cliente nuovo, non solo per il primo (BOT-42)"
```

> Avete in `tests/` il test `test_benvenuto10_valido_dopo_reset` con `xfail(strict=True)` (Lab 2 di oggi, i difetti noti)? Con l'app accesa adesso passa: **XPASS**, e la suite diventa rossa. È il registro dei difetti che funziona: togliete il decoratore `xfail` da quel test.

**Documentate.** Create `CHANGELOG.md` nella radice del repository (formato *Keep a Changelog*):

```markdown
# Changelog

## [Non rilasciato]

### Corretto
- BOT-42: BENVENUTO10 funzionava solo per il primo cliente nuovo dall'avvio del server.

### Modificato (refactoring, nessun cambiamento di comportamento)
- preventivo.py: via i print di debug, nomi parlanti, costanti al posto dei numeri magici.
```

Chi legge il CHANGELOG è un **umano** (il commerciale, un collega, voi tra sei mesi). Chi legge i messaggi di commit è anche una **macchina**. Servono entrambi.

**Una domanda per il cliente**, da scrivere in fondo al CHANGELOG sotto `### Da decidere`: dopo la correzione, un cliente nuovo può usare `BENVENUTO10` a **ogni** ordine. È giusto, o deve valere una volta per cliente? Non lo decidete voi.

Alla fine `git log --oneline` deve raccontare il lavoro, dal basso verso l'alto:

```
docs: CHANGELOG
fix: BENVENUTO10 vale per ogni cliente nuovo, non solo per il primo (BOT-42)
refactor: costanti al posto dei numeri magici
refactor: nomi parlanti
refactor: rimuovi print di debug
test: golden master di preventivo.calcola_totale
test: characterization test di preventivo.py
```

## Livello 3: la richiesta del commerciale (facoltativo)

1. **Passo 4 del refactoring (*Extract Function*).** Il calcolo della spedizione (dalla riga del CAP fino a `spedizione = 0`) diventa una funzione `_costo_spedizione(totale, cap, spedizione)` che restituisce la spedizione. Il corpo **c'è già**: tagliatelo e incollatelo, senza riscriverlo. Gabbia verde, commit.
2. **CR-07 in TDD (manutenzione evolutiva).**

   > **📝 Richiesta di modifica CR-07** · *ufficio commerciale*
   > "Dal prossimo rilascio i clienti VIP non pagano MAI la spedizione, isole comprese. Per tutti gli altri non cambia niente."

   - **RED**: `tests_preventivo/test_cr07_spedizione_vip.py`, un test parametrizzato su Firenze, Cagliari e Palermo per un VIP con 20 € di spesa (atteso 19,00: 20 € meno il 5%, spedizione 0), e un test che dimostra che per un cliente `nuovo` non cambia niente (24,90 a Firenze, 29,90 a Cagliari, con corriere a 4,90). I primi rossi, il secondo verde.
   - **GREEN**: modificate `_costo_spedizione` (ecco a cosa serviva estrarla: la modifica è in un punto solo). Le serve sapere se il cliente è VIP: aggiungete un parametro alla funzione **privata**, non a `calcola_totale`.
   - **La gabbia protesta, e questa volta va approvata.** Il golden master è rosso: quasi 700 casi cambiati. Prima di approvare controllate che siano **tutti e soli** casi `"tipo": "vip"`. Poi `pytest tests_preventivo --approva`, `git diff --stat`, e leggete un pezzo del diff. Chi approva un golden master senza leggere il diff ha appena spento la gabbia.
   - Commit `feat: spedizione gratuita per i clienti VIP (CR-07)` e riga nel CHANGELOG sotto `### Aggiunto`.
3. **Domanda da annotare nel CHANGELOG:** BOT-42 e CR-07 sono due tipi diversi di manutenzione. Quali? E il timeout che avete messo sul corriere, di che tipo era?

> Per chi è curioso: esiste anche il **mutation testing** (in Python, per esempio `mutmut`): un programma modifica apposta il vostro codice in tanti piccoli modi e controlla se i test se ne accorgono. Non lo facciamo, ma è il modo per capire se una gabbia è davvero stretta.

## Problemi frequenti

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| `ModuleNotFoundError: No module named 'preventivo'` | avete lanciato `pytest` da un'altra cartella | dalla radice del repository, dove c'è `pytest.ini` |
| `pytest` si ferma con "server spento" | avete scritto solo `pytest`, che lancia `tests/` | `pytest tests_preventivo` |
| `unrecognized arguments: --approva` | `conftest.py` non è in `tests_preventivo/`, o manca la cartella nel comando | copiate `conftest.py` dallo starter; `pytest tests_preventivo --approva` |
| `No module named 'golden_master'` | `golden_master.py` non è nella stessa cartella del test | tutti e tre i file dello starter vanno in `tests_preventivo/` |
| `assert 4032 == 4` (o simile) | avete cambiato le manopole (`DATE`, `CARRELLI`) dopo l'approvazione | sono cambiati i **casi**: se è voluto, `--approva` di nuovo e commit |

## Documentazione

- Michael Feathers, *Characterization testing*: https://michaelfeathers.silvrback.com/characterization-testing
- Approval testing (concetto): https://approvaltests.com/
- Martin Fowler, *Catalog of Refactorings*: https://refactoring.com/catalog/
- `itertools.product`: https://docs.python.org/3/library/itertools.html#itertools.product
- `unittest.mock`, dove applicare il patch: https://docs.python.org/3/library/unittest.mock.html#where-to-patch
- Keep a Changelog: https://keepachangelog.com/it-IT/1.1.0/
- Conventional Commits: https://www.conventionalcommits.org/it/v1.0.0/
- Floating point, problemi e limiti: https://docs.python.org/3/tutorial/floatingpoint.html
