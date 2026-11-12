# Simulazione 3 (livello esame): VeloCity

Una simulazione per allenarvi **a casa**, con la stessa struttura dell'esame del 25/11: 30 minuti di teoria, 90 di pratica. È al **livello dell'esame**: meno lacune, e alcuni test da scrivere per intero. Fatela dopo la simulazione 2, come una prova vera.

| Parte | Tempo | File |
|-------|-------|------|
| Teoria: 10 domande | 30 minuti | [`teoria.md`](teoria.md); le lettere in `RISPOSTE.md` |
| Pratica: 2 esercizi | 90 minuti | il testo è [`pratica.md`](pratica.md); il codice in `es1/` e `es2/` |

**Prendete il cronometro** e usate solo quello che avrete all'esame: il [cheat sheet](../CHEATSHEET.md) e [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md). Niente internet, niente AI: serve a voi, per sapere cosa ripassare.

## Preparazione

1. Copiate la cartella `simulazione_3/` **fuori** dal repository del corso (per esempio sul Desktop).
2. Spegnete la Bottega, se è accesa: il server di VeloCity usa la stessa porta, la 8000.
3. Usate il venv della Bottega: ha già `pytest`, `requests`, `flask` e `jsonschema`.

```bash
# Terminale 1: il server di VeloCity (resta acceso; è una scatola nera, non si apre)
cd simulazione_3
python server_velocity.py

# Terminale 2: i test
cd simulazione_3/es1 && pytest -v        # Esercizio 1
cd ../es2 && pytest -v                   # Esercizio 2
```

## Come si lavora

- Ogni `LACUNA(n)` va **sostituita** con quello che chiede la lacuna `(n)` del testo. Finché c'è, il test che la usa fallisce con `la lacuna (n) non è ancora completata`.
- Dove il file dice «scrivete qui il test», scrivete la funzione intera, con il pattern Arrange-Act-Assert.
- Lanciate `pytest -v` spesso. **Ma attenzione:** verde non vuol dire giusto. Un test senza `assert` è sempre verde, e all'esame conta la logica.
- Le risposte aperte (lacuna 14 e 2B.4) vanno in `RISPOSTE.md`.
- Quando avete finito, tutti i test devono essere verdi anche lanciando `pytest` due volte di fila (con le soluzioni di riferimento: `es1` **9 passed**, `es2` **5 passed**).

Le soluzioni escono **mercoledì 18/11** in `esame-semestre2/soluzioni_simulazione_3/`. Segnate i dubbi: li riprendiamo il 25/11 prima dell'esame.
