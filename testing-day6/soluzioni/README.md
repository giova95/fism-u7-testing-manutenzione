# Soluzioni del Giorno 6 (Lab 1 e Lab 2)

Qui trovate le soluzioni del **Lab 1** e del **Lab 2**, tutti i livelli: anche il Livello 3 del Lab 2 (il checkout che scala lo stock, il carrello vuoto). Le soluzioni del **Lab 3** (il corriere e i mock) sono in [`../../testing-day7/soluzioni/`](../../testing-day7/soluzioni/).

## Come usarle

- `tests/`: copiate i file nella cartella `tests/` della **vostra** Bottega (non sostituite i vostri: confrontateli) e lanciate `pytest` con corriere e app accesi.
- `bottega_fix/app.py`: l'app corretta. Cercate `[FIX G1]` per trovare le correzioni. `bottega_fix/spedizioni.py` è ancora quello originale: la sua correzione è il Lab 3.

## "Ma ci sono dei test rossi!"

Sì, ed è giusto così. Sulla Bottega **originale** sono rossi 14 test su 30:

- **8 del Lab 1**: 500 invece di 400 con il JSON rotto, 404 in HTML invece che in JSON;
- **4 sad path del carrello**: quantità negativa, zero, stringa e campo mancante vengono accettati (`201`) o fanno esplodere il server (`500`);
- **2 login falliti**: il messaggio dice se l'utente esiste.

Un test rosso che dimostra un bug è un documento di collaudo, non un errore del test. Con `bottega_fix/app.py` diventano tutti verdi (30 su 30).

## La fixture `stato_pulito`

È in `conftest.py`. Provate a toglierle `autouse=True` e lanciate `pytest`: `test_aggiunta_visibile_leggendo_il_carrello` diventa rosso con `assert 4 == 2`, perché un test precedente ha già messo 2 mouse nel carrello.

## Perché `base_url` ha `scope="session"`

Il controllo che il server sia acceso si fa una volta sola, non prima di ogni test. C'è anche un secondo motivo, che si vede con Playwright: i suoi test con il browser vogliono una `base_url` di sessione. Se un test con il browser trova la nostra "di funzione", si ferma con `ScopeMismatch`. I test delle API non ne sono toccati.
