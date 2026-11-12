# Simulazione 2 (guidata): il Cinema Aurora

Una simulazione per allenarvi **a casa**, con la stessa struttura dell'esame del 25/11: 30 minuti di teoria, 90 di pratica. È **guidata**: quasi tutto è a lacune, come l'esame vero. Fatela prima della simulazione 3, che è un po' più difficile.

| Parte | Tempo | File |
|-------|-------|------|
| Teoria: 10 domande | 30 minuti | [`teoria.md`](teoria.md); le lettere in `RISPOSTE.md` |
| Pratica: 2 esercizi | 90 minuti | il testo è [`pratica.md`](pratica.md); il codice in `es1/` e `es2/` |

**Prendete il cronometro** e usate solo quello che avrete all'esame: il [cheat sheet](../CHEATSHEET.md) e [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md). Niente internet, niente AI: serve a voi, per sapere cosa ripassare.

## Preparazione

1. Copiate la cartella `simulazione_2/` **fuori** dal repository del corso (per esempio sul Desktop).
2. Spegnete la Bottega, se è accesa: il server del cinema usa la stessa porta, la 8000.
3. Usate il venv della Bottega: ha già `pytest`, `requests`, `flask` e `jsonschema`.

```bash
# Terminale 1: il server del cinema (resta acceso; è una scatola nera, non si apre)
cd simulazione_2
python server_cinema.py

# Terminale 2: i test
cd simulazione_2/es1 && pytest -v        # Esercizio 1
cd ../es2 && pytest -v                   # Esercizio 2
```

## Come si lavora

- Ogni `LACUNA(n)` va **sostituita** con quello che chiede la lacuna `(n)` del testo. Finché c'è, il test che la usa fallisce con `la lacuna (n) non è ancora completata`.
- Lanciate `pytest -v` spesso. **Ma attenzione:** verde non vuol dire giusto. Un test senza `assert` è sempre verde, e all'esame conta la logica.
- Le risposte aperte (lacuna 18 e 2B.4) vanno in `RISPOSTE.md`.
- Quando avete finito: `es1` deve dare **9 passed**, `es2` **5 passed**, anche lanciando `pytest` due volte di fila.

Le soluzioni escono **mercoledì 18/11** in `esame-semestre2/soluzioni_simulazione_2/`. Segnate i dubbi: li riprendiamo il 25/11 prima dell'esame.
