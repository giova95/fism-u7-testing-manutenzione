# SIMULAZIONE DI ESAME: Parte Pratica (90 minuti)

Scrivete le soluzioni a penna. Valuto la struttura Arrange-Act-Assert e il disaccoppiamento.

### ESERCIZIO 1: White Box (Gestione Eccezioni)

Avete il seguente modulo termometro.py:

```python
def valida_temperatura(gradi: int) -> str:
    if gradi < -273:
        raise ValueError("Temperatura sotto lo zero assoluto. Impossibile.")
    return "Lettura termica valida."
```

**TASK**
Scrivete test_termometro.py. Create due test:

Testa una temperatura valida (es. 20)

Testa una temperatura non valida (es. -300) usando pytest.raises per verificare l'eccezione

### ESERCIZIO 2: Mocking (Isolamento Dipendenze)

Avete il modulo meteo.py:

```python
from sensore_esterno import leggi_umidita

def allarme_pioggia() -> str:
    umidita = leggi_umidita()
    if umidita > 90:
        return "Allarme: Pioggia imminente!"
    return "Cielo sereno."
```

**TASK**
Scrivete test_meteo.py: vi serve un solo test per simulare il caso di allarme pioggia
Utilizzate @patch per intercettare la funzione leggi_umidita e forzarla a restituire 95

### ESERCIZIO 3: Black Box (Subprocess e Standard POSIX)

Avete sviluppato uno script CLI chiamato ping.py. Non potete leggerne il codice, ma conoscete le sue specifiche di sistema:

Comando: python ping.py <PAROLA>

- Se passate la parola "hello", stampa su standard output "Pong!" ed esce con Exit Code 0

- Se non passate nessuna parola o passate una parola diversa, stampa su standard error "Errore di comunicazione" ed esce con Exit Code 1

**TASK**
Scrivete test_ping.py usando subprocess.run(). Create due funzioni di test:

Una che invoca lo script con "hello" e verifica l'Exit Code e l'Output.

Una che invoca lo script con una parola sbagliata (es. "ciao") e verifica l'Exit Code e lo Stderr
