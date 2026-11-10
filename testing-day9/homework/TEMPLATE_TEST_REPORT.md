# Test Report · La Bottega · Rilascio del <gg/mm/aaaa>

> **Regola d'oro: UNA pagina.** Se non ci sta, state scrivendo per voi, non per chi deve decidere.
> Niente gergo: chi legge sa cos'è un cliente, un euro e un rischio. Non sa cos'è una fixture.

| | |
|---|---|
| **Versione** | commit `<sha corto>` · branch `main` |
| **Data del collaudo** | <gg/mm/aaaa> |
| **Redatto da** | <nome e cognome> |
| **Destinatario** | CTO, La Bottega |
| **Report tecnici completi** | <«report HTML prodotto in locale il gg/mm», oppure il link alla run di GitHub Actions> |

## 1. In una frase

> <Esempio di forma: «La versione X è pronta per la produzione con 2 difetti noti di gravità media; raccomandiamo il rilascio **a condizione che** ... entro ...»>

## 2. Perimetro: cosa abbiamo verificato (e cosa NO)

| Verificato | Come |
|------------|------|
| <es. il contratto delle API: catalogo, login, carrello, ordini> | <es. test automatici dall'esterno, come un cliente> |
| <...> | <...> |

**Fuori perimetro** (non verificato, e quindi rischio non misurato): <es. carico con 600 ordini/ora del Black Friday; browser diversi da Chromium; ...>

## 3. Ambiente

<Dove sono girati i test: es. "server di integrazione automatico (GitHub Actions, Ubuntu, Python 3.14), ad ogni modifica del codice"; dati di prova; versione del fornitore SpediVeloce (simulato).>

## 4. Risultati

| Esito | Numero | Cosa significa |
|-------|-------:|----------------|
| Superati | | il comportamento è quello concordato |
| Falliti | | difetti **nuovi**, non ancora analizzati |
| Difetti noti | | difetti **conosciuti e registrati**, con un responsabile |
| Non eseguiti | | controlli oggi impossibili, con il motivo |

## 5. Difetti aperti, per gravità

| ID | Cosa vede il cliente (o l'azienda) | Gravità | Impatto stimato | Proposta |
|----|------------------------------------|---------|-----------------|----------|
| | | Bloccante / Alta / Media / Bassa | €/mese o clienti/mese | correggere ora / dopo / decidere |

## 6. Rischi residui

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| | Alta / Media / Bassa | Alto / Medio / Basso | |

## 7. Raccomandazione

**☐ GO   ☐ GO CONDIZIONATO   ☐ NO-GO**

Interventi proposti (i conti al mese):

| Intervento | Costo (giornate × 400 €) | Non fare niente costa (€/mese) | Si ripaga in |
|------------|-------------------------:|-------------------------------:|-------------:|
| <es. refactoring di `preventivo.py`> | | | |
| <es. protezione dal corriere lento> | | | |

Condizioni (se GO condizionato): <cosa deve succedere, chi lo fa, entro quando>

Decisioni richieste alla CTO: <es. DEC-001: la maggiorazione isole si applica anche con la spedizione gratuita? Risposta entro il ...>
