# Lab 1: Il Game Designer

## Contesto Aziendale

Siete stati assunti come Backend Engineer per un nuovo videogioco di ruolo (GDR). Il Game Designer vi ha consegnato la funzione logica che permette ai personaggi di equipaggiare armi e artefatti magici. Il vostro compito è blindare questa funzione con una suite di test, portarla in cloud e sopravvivere a un improvviso cambio di specifiche che farà esplodere la vostra infrastruttura.

## Task

### Step 1: Il Codice Sorgente

Nel vostro repository, create la cartella gdr e al suo interno il file armeria.py. Copiate questo codice. Leggetelo attentamente: le regole di business nascondono insidie.

```python
def equipaggia_artefatto(guerriero: dict, artefatto: dict) -> str:
    """Logica di equipaggiamento per un personaggio GDR."""

    if guerriero.get("hp", 0) <= 0:
        raise ValueError("Un guerriero caduto non può equipaggiare oggetti.")

    if guerriero["livello"] < artefatto["livello_minimo"]:
        raise ValueError(f"Livello troppo basso. Richiesto: {artefatto['livello_minimo']}")

    if artefatto.get("classe_esclusiva") and guerriero["classe"] != artefatto["classe_esclusiva"]:
        raise PermissionError(f"Questo oggetto è riservato alla classe {artefatto['classe_esclusiva']}.")

    if artefatto.get("maledetto", False) and guerriero["allineamento"] == "buono":
        return "L'artefatto brucia! Equipaggiamento fallito."

    guerriero["equipaggiamento"].append(artefatto["nome"])
    return f"{artefatto['nome']} equipaggiato con successo."
```

### Step 2: Scrittura Test in Autonomia

Create test_armeria.py, dovete scrivere una suite di test (usando pytest e possibilmente @pytest.mark.parametrize per non duplicare codice) che copra ogni singola diramazione di questa funzione.
Il codice non può andare in produzione se non avete il 100% di Branch Coverage.
Per verificarlo, lanciate nel terminale:
pytest --cov=armeria --cov-branch --cov-report=term-missing

### Step 3: L'Infrastruttura in Cloud (La Pipeline)

Avete il 100% di coverage sul vostro PC? Bene, ora dimostratelo al server.

1. Create requirements.txt

2. Create .github/workflows/ci.yml e inserite il codice standard della pipeline:

```yaml
name: Pipeline di Validazione
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - run: |
          pytest --cov=. --cov-branch --cov-report=term
```

3. Eseguite git add ., git commit -m "ci: setup test armeria" e git push

4. Andate su GitHub e la vostra Action deve essere VERDE

### Step 4: Il Sabotaggio del Game Designer

Il gioco è online. Il Game Designer irrompe nel vostro ufficio: "I giocatori hanno trovato un exploit! Gli artefatti maledetti non devono bruciare solo i personaggi buoni. Devono bruciare tutti quelli che non sono esplicitamente malvagi!"

Dovete cambiare il codice sorgente:

1. Aprite armeria.py.

2. Modificate la riga maledetta in questo modo:
   DA: if artefatto.get("maledetto", False) and guerriero["allineamento"] == "buono":
   A: if artefatto.get("maledetto", False) and guerriero["allineamento"] != "malvagio":

3. Siete in emergenza. Sbagliate procedura: non lanciate i test in locale e committate direttamente:

```bash
 git add armeria.py
 git commit -m "fix: bilanciamento danni artefatti maledetti"
 git push
```

### Step 5: Leggere i Log e Risolvere

Andate su GitHub e vedete che la pipeline è appena esplosa, il pallino è ROSSO.
Il vostro codice ha un bug strutturale: la nuova regola di business ha distrutto i vecchi test.

**Il vostro Task Finale:**

1. Non andate a tentativi sul vostro editor. Aprite il log del fallimento su GitHub Actions.

2. Leggete l'errore sollevato da pytest, vi dirà esattamente cosa succede

3. Tornate in locale. Modificate i dati nei vostri test in test_armeria.py affinché rispettino la nuova feature imposta dal Game Designer

4. Pushate il fix (git add ., git commit -m "test: allineamento a nuova patch di bilanciamento", git push)

5. Assicuratevi che il Quality Gate in cloud torni VERDE

### REMINDER

Per questo homework non è prevista la consegna ma è fortemente consigliato lo svolgimento in vista della prova finale
