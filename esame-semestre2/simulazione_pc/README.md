# Simulazione d'esame al PC (mercoledì 11/11, 13:00–15:00)

Stessa struttura dell'esame del 25/11, ma al computer: così vedete subito se un test è verde o rosso. **All'esame vero sarete su carta**: la logica è la stessa.

| Parte | Tempo | Dove |
|-------|-------|------|
| Teoria: 10 domande | 13:00–13:30 | [`../simulazione_teoria.md`](../simulazione_teoria.md); le lettere in `RISPOSTE.md` |
| Pratica: 2 esercizi | 13:30–15:00 | il testo è [`../simulazione_pratica.md`](../simulazione_pratica.md); il codice in `es1/` e `es2/` |

## Regole

- Potete usare il [cheat sheet](../CHEATSHEET.md) e [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md). Niente internet, niente AI, niente compagni: è una prova per **voi**, per sapere cosa ripassare.
- Il server è una **scatola nera**: `server_biblioteca.py` si avvia e basta, **non si apre**. Il riferimento è il contratto stampato nel testo.

## Preparazione (5 minuti)

1. Copiate la cartella `simulazione_pc/` **fuori** dal repository della Bottega (per esempio sul Desktop).
2. **Spegnete la Bottega** (`CTRL+C` nei terminali di `app.py` e `corriere.py`): il server della biblioteca usa la stessa porta, la 8000.
3. Usate il venv della Bottega: ha già `pytest`, `requests`, `flask` e `jsonschema`.

```bash
# Terminale 1: il server della biblioteca (resta acceso)
cd simulazione_pc
python server_biblioteca.py

# Terminale 2: i test
cd simulazione_pc/es1 && pytest -v        # Esercizio 1
cd ../es2 && pytest -v                    # Esercizio 2
```

## Come si lavora

- Ogni `LACUNA(n)` va **sostituita** con quello che chiede la lacuna `(n)` del testo. Finché c'è, il test che la usa fallisce con `la lacuna (n) non è ancora completata`.
- Dove il file dice «scrivete qui il test», scrivete la funzione intera, con il pattern Arrange-Act-Assert.
- Lanciate `pytest -v` spesso: un test che diventa verde vi dice che siete sulla strada giusta. **Ma attenzione:** verde non vuol dire giusto. Un test senza `assert` è sempre verde, e all'esame conta la logica.
- Le risposte aperte (lacuna 15 e 2B.4) vanno in `RISPOSTE.md`.

## Consegna (entro le 15:00)

Copiate la cartella `simulazione_pc/` nel vostro repository privato, poi:

```bash
git add simulazione_pc
git commit -m "simulazione d'esame"
git push
```

Non è valutata. Le soluzioni escono alle 15:00, in `esame-semestre2/soluzioni_simulazione/`: correggetevi da soli a casa e segnate i dubbi. Li riprendiamo il 25/11 prima dell'esame.
