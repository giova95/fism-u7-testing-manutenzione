# Soluzioni del compito della G2 (Lab 3: il corriere)

Qui trovate le soluzioni del [Lab 3](../../testing-day6/lab3_dipendenze_esterne/README.md), cioè del compito della G2.

| File | Cosa contiene |
|------|---------------|
| `lab_dipendenze_esterne/test_lab3_spedizioni.py` | i test con il mock (Livelli 1 e 2): costo letto dalla risposta, CAP e peso giusti, timeout, guasti di rete e `503` che diventano `ServizioSpedizioniNonDisponibile` |
| `lab_dipendenze_esterne/spedizioni.py` | la correzione: `timeout`, controllo dello status, eccezione di dominio |
| `lab_dipendenze_esterne/app.py` | il checkout che risponde `503` quando il corriere non c'è, **senza** toccare stock e carrello |
| `lab_dipendenze_esterne/test_lab3_esperimento_chaos.py` | l'esperimento di chaos (Livello 3, facoltativo) |

## Come usarle

1. Copiate `test_lab3_spedizioni.py` nella cartella `tests/` della vostra Bottega e lanciatelo **con app e corriere spenti**: sul vostro codice corretto deve essere verde. Sul codice originale si ferma con un errore di collection (`ImportError`): la classe `ServizioSpedizioniNonDisponibile` non esiste ancora.
2. Confrontate il vostro `spedizioni.py` con quello della soluzione. Non deve essere identico: deve far passare gli stessi test.
3. L'esperimento di chaos si lancia con app e corriere accesi: `pytest -m chaos`. Provatelo con il corriere **spento** e con il corriere **lento** (`CORRIERE_LATENZA=10 python corriere.py`), prima e dopo la correzione.

| Codice | Corriere spento | Corriere lento (10 s) |
|--------|-----------------|------------------------|
| originale | rosso: `500` invece di `503` | rosso: `201` dopo 10 secondi |
| corretto | verde, subito | verde, `503` in circa 3 secondi |

La Bottega con tutte le correzioni (Lab 1, 2 e 3) è in [`../../testing-day8/bottega_start/`](../../testing-day8/bottega_start/).
