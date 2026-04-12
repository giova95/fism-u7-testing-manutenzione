# Esercizio 3: La Banca e l'Automazione

## Contesto Aziendale

Benvenuti in produzione. Cercare bug a occhio nudo come nell'esercizio precedente costa tempo e soldi.
Il file `banca.py` contiene errori critici di logica, di validazione e problemi matematici di precisione (i classici nemici delle banche).
Ma questa volta, abbiamo la suite di test automatizzata

## Task

0. Attiva ambiente virtuale di python:

```
python -m venv venv

#Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

```

1. Assicurati di aver installato pytest: `pip install -r ../requirements.txt`
2. **NON guardare il file `banca.py`**.
3. Non modificare i test in `test_banca.py`. I test rappresentano la "Verità Assoluta" (i requisiti di business)
4. Apri il terminale: `pytest test_banca.py -v`
5. Leggi con attenzione i messaggi di errore rossi (Traceback).
6. Correggi `banca.py` finché non ottieni un "PASSED" verde per ogni singolo test.
