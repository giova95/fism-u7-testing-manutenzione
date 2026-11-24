# Postmortem: <titolo breve e fattuale, es. "Checkout fallito a metà per instabilità del corriere">

> **Blameless.** Questo documento descrive cosa è successo e perché il **sistema** lo ha permesso.
> Non contiene colpevoli: se una persona ha "sbagliato", la domanda giusta è *perché il sistema le ha permesso di farlo così facilmente?*

| Campo | Valore |
|-------|--------|
| Data | 25/11/2026 |
| Squadra | |
| Autore | |

## 1. Sommario (massimo 3 righe, per un capo che non sa cos'è un 503)

*Cosa ha visto il cliente, per quanto tempo, cosa ci è costato.*

## 2. Timeline

Le ore da `INCIDENTE.md`, il file dello Scriba della vostra squadra.

| Ora | Cosa è successo | Fonte (misura.py / pytest / browser / curl / log) |
|-----|-----------------|---------------------------------------------------|
| | Inizio dell'indagine | cronometro |
| | **RILEVATO:** ... | |
| | **DIAGNOSI** consegnata | |

## 3. Causa: i 5 perché

Partite dal sintomo e chiedete "perché?" finché non arrivate a qualcosa che si può **correggere nel sistema** (bastano 3-5 righe).

1. Perché i clienti non riuscivano a ...? Perché ...
2. Perché ...?
3. Perché ...?

## 4. Due azioni correttive

Ogni azione ha **un** responsabile (owner). Un'azione senza owner non la fa nessuno.

| # | Azione | Owner |
|---|--------|-------|
| 1 | es. Lanciare `misura.py` ogni ora e avvisare se il checkout supera l'1% di errori | |
| 2 | | |

## 5. Lezione imparata

*(1-2 frasi che vorreste far leggere a un collega prima del suo primo turno di reperibilità)*
