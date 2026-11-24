# LAB 1 — L'esperimento: misuro, rompo, rimisuro

> 📖 **Parole da sapere per questo lab** (spiegate con esempi in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [latenza](../../CONCETTI_BASE.md#latenza) · [media e percentile](../../CONCETTI_BASE.md#media-e-percentile) · [Chaos Engineering](../../CONCETTI_BASE.md#chaos-engineering)

> **Si fa tutto in aula, passo per passo insieme al docente** (circa 15 minuti). Non si scrive codice: si lanciano comandi, si leggono numeri e si scrivono le risposte in un file.

## Contesto

In aula avete già visto il corriere **spento** e il corriere **lento**: la Bottega risponde con un 503 pulito. Oggi proviamo il guasto più comune nella realtà: il fornitore **instabile**, che risponde bene due volte su tre e male la terza.

Non "proviamo a vedere cosa succede": facciamo un **esperimento**, con il metodo scientifico.

```
1. com'è fatto SANO?  →  2. IPOTESI  →  3. ROMPO (una cosa sola)  →  4. RIMISURO  →  5. verificata o FALSIFICATA?
```

**Prima di iniziare:** corriere (terminale 1) e Bottega (terminale 2) accesi, come nel `SETUP.md`. Nel terminale 3 controllate che non ci siano guasti attivi:

```bash
python chaos_ctl.py stato
```
→ `Nessun guasto attivo.`

Create un file `ESPERIMENTI.md` nella cartella `bottega_g5`: le risposte vanno lì.

## Passo 1 — Com'è fatto "sano"?

Prima di rompere qualcosa bisogna sapere com'è fatto quando **non** è rotto: nel Chaos Engineering si chiama **stato stazionario**. Senza una misura di partenza, dopo l'esperimento potete dire solo "mi sembra lento".

```bash
python misura.py
```

Vedrete una tabella come questa (i numeri cambiano un po' da PC a PC):

```text
endpoint             richieste   errori     p50     p95     max   status
GET /api/prodotti          100     0.0%   0.01s   0.02s   0.03s   {200: 100}  ok
POST /api/carrello          20     0.0%   0.01s   0.02s   0.05s   {201: 20}  ok
POST /api/ordini            20     0.0%   0.01s   0.02s   0.06s   {201: 20}  ok

Ipotesi: errori <= 1.0% e p95 <= 1.0s su ogni endpoint
VERDETTO: ipotesi VERIFICATA
```

Come si legge una riga:

| Colonna | Cosa vuol dire |
|---------|----------------|
| **errori** | quante richieste sono fallite (5xx o nessuna risposta) |
| **p50** | il tempo del cliente **tipico**: metà delle richieste è stata più veloce |
| **p95** | il tempo del cliente **sfortunato**: 95 richieste su 100 sono state più veloci di così |
| **status** | gli status code ricevuti, con quante volte ciascuno |

> Perché p50 e p95 e non la **media**? Perché la media mente: 99 risposte da 0,01 secondi e una da 10 secondi fanno una media di 0,11 secondi, "ottima". Ma un cliente su cento ha aspettato 10 secondi.

## Passo 2 — L'ipotesi

Si scrive **prima** di rompere, non dopo. Copiatela in `ESPERIMENTI.md`:

```markdown
## Esperimento — corriere instabile
- **Ipotesi:** con il 30% di errori del corriere, il checkout resta sano (errori <= 1%)
- **Cosa rompo:** il corriere, che sbaglia il 30% delle risposte (una cosa sola)
- **Dove:** solo sul mio PC
- **Come lo fermo:** CTRL+C sul corriere e riavvio senza opzioni
```

Secondo voi regge o non regge? Scrivetelo accanto all'ipotesi, prima di andare avanti: non c'è risposta sbagliata.

## Passo 3 — Rompo

```bash
# Terminale 1: CTRL+C sul corriere, poi
python chaos_ctl.py corriere --errori 0.3
```

## Passo 4 — Rimisuro

```bash
# Terminale 3
python misura.py --checkout 100
```

(`--checkout 100` fa 100 acquisti invece di 20: con un guasto che capita "ogni tanto", più prove = numero più affidabile.)

Guardate la riga `POST /api/ordini` e l'ultima riga, `VERDETTO`.

## Passo 5 — Rimetto a posto

```bash
# Terminale 1: CTRL+C, poi
python chaos_ctl.py corriere
# Terminale 3
python misura.py
```
→ di nuovo `VERIFICATA`. Un esperimento serio si può **fermare** in un attimo: è la differenza tra un esperimento e "rompere a caso".

## Le risposte in `ESPERIMENTI.md`

> 🧩 **Copiate questa traccia sotto l'ipotesi e sostituite i `???`** leggendo i numeri di `misura.py`:
>
> ```markdown
> ### Passo 1: il sistema sano (python misura.py)
> - checkout, riga `POST /api/ordini`: errori ???%   p95 ??? s
> - verdetto: ???
>
> ### Passo 4: con il corriere al 30% di errori (python misura.py --checkout 100)
> - checkout, riga `POST /api/ordini`: errori ???%
> - che status code riceve il cliente quando va male? ???
> - catalogo e carrello hanno errori? ???  Perché secondo voi? ???
> - verdetto: ???  → la mia ipotesi è ??? (verificata / falsificata)
>
> ### Cosa ho imparato
> - il cliente, su 100 acquisti, se ne vede fallire circa ???
> - come si potrebbe difendere la Bottega? (una frase, a parole vostre) ???
> ```
>
> **Trucco:** se al passo 4 gli errori sono 0%, il corriere è ancora quello sano: nel terminale 1 avete lanciato `python chaos_ctl.py corriere --errori 0.3`?

**Obiettivo del lab:** `ESPERIMENTI.md` con l'ipotesi e la traccia compilata. È anche il primo punto del compito.

## Documentazione

- Principles of Chaos Engineering: https://principlesofchaos.org/
- Percentili e latenza ("la media mente"), Google SRE Book, cap. 4 *Service Level Objectives*: https://sre.google/sre-book/service-level-objectives/
