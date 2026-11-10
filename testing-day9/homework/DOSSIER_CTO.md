# Il dossier per la CTO

> 📖 **Parole da sapere** (in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md)): [debito tecnico](../../CONCETTI_BASE.md#debito-tecnico) · [refactoring](../../CONCETTI_BASE.md#refactoring) · [timeout](../../CONCETTI_BASE.md#timeout)

Questo file serve per il **Test Report** del compito (`README.md`, Livello 1, punto 2). Contiene i dati dell'azienda: usateli per la sezione 7 del report, quella con i costi e i benefici.

## La situazione

La **CTO della Bottega** vi ha scritto una riga sola: *«Venerdì si va in produzione? Sì o no.»* Deve decidere tre cose:

1. **Si va in produzione** con la versione attuale? (Il Black Friday è il 27 novembre.)
2. Vale la pena pagare **2 giornate di refactoring** di `preventivo.py`, il codice di Gianni che avete visto in aula? «Funziona da sette anni.»
3. Il **timeout con il 503** sul corriere: «Ci serve davvero? A me sembra che così perdiamo ordini.»

La CTO ha scritto codice fino a dieci anni fa. Non sa cosa sia una fixture e non le interessa. Le interessano tre cose: **soldi, clienti, rischi**. Leggerà il vostro report in un minuto, tra una riunione e l'altra.

## Le regole del report

1. **Niente gergo.** Ogni parola tecnica va tradotta: "status 500" si scrive «il sito va in errore»; "xfail" si scrive «difetto noto e registrato»; "mock" non serve proprio.
2. **Ogni affermazione ha un numero.** "Il refactoring fa risparmiare tempo" non vale niente. "Il refactoring costa 800 euro e si ripaga in circa 3 mesi" vale.
3. **Voi raccomandate, la CTO decide.** Non scrivete «bisogna fare così». Scrivete: «Le opzioni sono A e B, costano tanto, rischiano tanto: raccomandiamo A, perché...».
4. **Mai nascondere un rischio.** Se un rischio non è coperto dai test, scrivetelo voi.
5. Se vi serve un dato che non c'è, dichiarate l'**ipotesi** («ipotizziamo che...»).

## I dati dell'azienda

| Dato | Valore |
|------|--------|
| Ordini al giorno (media) | 150 |
| Scontrino medio | 78 € |
| Ore di punta | il 70% degli ordini arriva tra le 18 e le 23 |
| Black Friday (24-30 novembre) | ordini **× 4** |
| Costo di una giornata di uno sviluppatore | 400 € |

## I risultati dei test

Usate i numeri **veri** della vostra ultima run su `main` (Lab 2: la tabella passati / falliti / difetti noti / saltati). Se non li avete, questi sono quelli della Bottega di partenza:

| Esito | Numero |
|-------|-------:|
| Passati | 37 |
| Falliti | 0 |
| Difetti noti | 2 |
| Saltati | 1 |

## Difetti e questioni aperte

| ID | Cosa succede (in linguaggio tecnico) | Dati utili |
|----|--------------------------------------|------------|
| **BUG-009** | Il codice `BENVENUTO10` è salvato in una lista globale: vale **una volta per tutto il server**, non per cliente (è il ticket BOT-42 visto in aula) | Campagna "BENVENUTO10" già pagata: **3.000 €** di pubblicità. Attesi **400 nuovi clienti al mese** |
| **DEC-001** | Sopra i 49,99 € la spedizione è gratuita e la **maggiorazione isole di 5 €** sparisce | L'**8%** degli ordini va verso le isole; di questi il **65%** supera 49,99 €. Il commerciale nel 2022 aveva chiesto "+5 € per le isole". Nessuno ha mai scritto se valesse anche con la spedizione gratuita |
| **BUG-010** | Lo sconto `BLACKFRIDAY` dipende dalla data di sistema e **non è testato** | Il Black Friday è tra due settimane. Nel 2025 il codice è stato modificato a mano il 23 novembre |

## Intervento 1: refactoring di `preventivo.py`

| Dato | Valore |
|------|--------|
| Stima del refactoring | **2 giornate** (la gabbia di test si fa nella prima mezza giornata) |
| Richieste di modifica del commerciale a `preventivo.py` negli ultimi 24 mesi | **7** |
| Tempo medio per una modifica oggi | **2 giornate** (paura di toccarlo, prove a mano) |
| Tempo stimato per una modifica dopo il refactoring | **0,5 giornate** |
| Incidenti in produzione causati da quelle modifiche | **3** in 24 mesi; il più grave: **1.800 €** di sconti applicati per errore |
| Effetto collaterale | insieme al refactoring si corregge anche **BUG-009** |

## Intervento 2: timeout e 503 sul corriere

| Dato | Valore |
|------|--------|
| Costo della correzione | **1 giornata** (già fatta: è il timeout che avete scritto) |
| SpediVeloce, episodi di lentezza nel 2025 | **5**, durata media **60 minuti**, di cui **2** nel weekend del Black Friday |
| Senza timeout, con il corriere lento | **tutto il sito** si blocca, anche il catalogo |
| Con il 503 | si blocca solo il pagamento; il carrello resta salvo; stimiamo che il **60%** dei clienti riprovi più tardi |
| Alternativa proposta dal team | **tariffa di riserva**: se il corriere non risponde, si applica una spedizione fissa di **9,90 €**. Stima: **1 giornata**. La tariffa vera può essere 4,90 € o 9,90 € |

## I conti, in tre formule

| Formula | Esempio di frase per la CTO |
|---------|-----------------------------|
| **Rischio = probabilità × impatto** | «Il Black Friday non testato è poco probabile che si rompa, ma se si rompe vale un weekend di vendite × 4.» |
| **Non fare niente costa** (in € al mese) | «Lasciare il codice com'è ci costa circa ... € al mese, perché ...» |
| **Break-even = costo ÷ risparmio al mese** | «L'intervento costa ... € e si ripaga in ... mesi.» |

> 🧩 **Non sai da dove partire con i conti del refactoring?** Tre domande, in ordine:
> 1. Quanto **costa** l'intervento? (giornate × 400 €)
> 2. Quanto si **risparmia al mese**? Le modifiche sono 7 in 24 mesi: quante al mese? Ognuna fa risparmiare 2 − 0,5 giornate. Quanti euro sono? E gli incidenti: 3 in 24 mesi, quanto valgono al mese se ne prendete come esempio uno da 1.800 €? (Scrivete l'ipotesi.)
> 3. **Costo ÷ risparmio al mese** = in quanti mesi si ripaga.
>
> Non esiste un solo risultato giusto: conta che i passaggi e le ipotesi siano scritti, così la CTO può controllarli.

## Documentazione

- ISO/IEC/IEEE 29119-3 (struttura standard della documentazione di test, il "Test Completion Report"): https://www.iso.org/standard/79429.html
- Martin Fowler, "Is High Quality Software Worth the Cost?": https://martinfowler.com/articles/is-quality-worth-cost.html
- Martin Fowler, Technical Debt: https://martinfowler.com/bliki/TechnicalDebt.html
