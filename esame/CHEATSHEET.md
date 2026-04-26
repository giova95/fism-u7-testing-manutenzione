# Foglio utilizzabile durante la parte pratica

Smettete di cercare di ricordare la sintassi a memoria. Usate questo documento come riferimento per tradurre la vostra logica in codice valido.

## 1. FONDAMENTI DI PYTHON

**Definizione di Funzioni e Type Hinting:**

```python
def mia_funzione(parametro: str, numero: int) -> bool:
    # Corpo della funzione
    return True
```

**Strutture Condizionali (If / Else)**

```python
if valore > 10:
    # fai qualcosa
elif valore == 5:
    # fai un'altra cosa
else:
    # caso di default
```

**Sollevare un'Eccezione (Freno di Emergenza):**

```python
if importo < 0:
    raise ValueError("L'importo non può essere negativo")
if utente_non_autorizzato:
    raise PermissionError("Accesso negato")
```

**Gestione Liste (Array):**

```python
# Inizializzazione e operazioni base
codici = ["A1", "B2", "C3"]
primo_elemento = codici[0]      # Legge "A1"
lunghezza = len(codici)         # Restituisce 3
codici.append("D4")             # Aggiunge in coda
```

**Cicli (Iterazioni):**

```python
# Iterare direttamente sugli elementi di una lista
for codice in codici:
    if codice == "B2":
        break  # Ferma il ciclo in anticipo

# Iterare su un range numerico (da 0 a 4)
for i in range(5):
    # Fai qualcosa 5 volte
    pass
```

## 2. PYTEST: ECCEZIONI E PARAMETRIZZAZIONE

**Intercettare un Errore (Sad Path):**

```python
import pytest

def test_errore_atteso():
    with pytest.raises(ValueError, match="Testo atteso"):
        funzione_da_testare(-10)
```

**La Matrice dei Dati (Parametrize + Nullcontext):**

```python
import pytest
from contextlib import nullcontext as does_not_raise

# Matrice: [ (Input, Contesto_Atteso, Output_Atteso) ]
@pytest.mark.parametrize("valore, aspettativa, risultato", [
    (-5, pytest.raises(ValueError), None),
    (10, does_not_raise(), "Successo")
])
def test_logica(valore, aspettativa, risultato):
    with aspettativa:
        assert funzione_da_testare(valore) == risultato
```

## 3. UNITTEST: ISOLAMENTO (MOCKING)

**Il Decoratore Patch:**
Attenzione al path: intercetta l'oggetto DOVE viene utilizzato, non dove è definito!

```python
from unittest.mock import patch

# 'file_di_business' e' il file che state testando
@patch('file_di_business.funzione_lenta_esterna')
def test_con_mock(mock_funzione):
    # 1. SETUP: Forza il mock a restituire un valore fisso
    mock_funzione.return_value = 100.0

    # 2. EXECUTION: Lancia la TUA funzione
    risultato = la_mia_funzione_da_testare()

    # 3. ASSERTION
    assert risultato == "OK"
```

**4. BLACK BOX TESTING (SISTEMA OPERATIVO)**

```python
import subprocess

def test_interazione_terminale():
    # Simulazione: python mio_script.py parametro1
    comando = ["python", "mio_script.py", "parametro1"]

    # Esecuzione del processo isolato
    risultato = subprocess.run(comando, capture_output=True, text=True)

    # Asserzioni POSIX
    assert risultato.returncode == 0                     # Exit Code
    assert "Successo" in risultato.stdout                # Standard Output
    assert "Errore" in risultato.stderr                  # Standard Error
```
