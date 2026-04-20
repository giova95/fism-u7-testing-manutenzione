# RECAP GIORNO 3: L'Arte dell'Isolamento e dell'Efficienza

Come avete visto scrivere un test che passa è facile, scrivere una suite di test che scala nel tempo, che non fallisce a caso e che non richiede manutenzione continua è Ingegneria del Software. Oggi abbiamo eliminato il debito tecnico (copia-incolla) e l'imprevedibilità. Di seguito i pattern architetturali trattati, da usare come standard per i vostri esercizi

## 1. Fondamenti Architetturali

Prima di scrivere asserzioni, dovete padroneggiare la struttura e le metriche production-ready

### A. Anatomia di un Test (Il Pattern AAA)

Ogni singolo test deve essere diviso logicamente in 3 fasi. (Riferimento: guardate le soluzioni in testing-day3/dado_per_mock/test_gioco.py):

1. **Setup (Arrange):** Preparazione dello stato iniziale (es. "Trucco il dado", "Preparo i dati di input")

2. **Execution (Act):** Chiamata della singola funzione logica che stiamo testando. Deve essere una singola azione

3. **Assertion (Assert):** Verifica del risultato e degli effetti attesi

### B. Strategie di Testing

- **Black Box Testing:** Trattate la funzione come una scatola chiusa. Vi interessa solo il contratto logico: cosa entra (Input) e cosa esce (Output). Non si guarda il codice sorgente

- **White Box Testing:** Aprite la scatola. Guardate le istruzioni, i cicli`for`, gli `if/else`, e scrivete test mirati per forzare il codice a passare attraverso ogni singola diramazione logica

### C. La Metrica della Verità: Branch Coverage

La _Code Coverage_ (Copertura delle righe) vi dice quante istruzioni sono state lette. È una metrica debole: avere il 100% di righe lette non significa aver testato la logica. I Senior misurano la **Branch Coverage**: questa metrica verifica che per ogni bivio decisionale (come un `if`) sia stato testato esplicitamente sia lo scenario `True` che lo scenario `False`

**Strumenti da Terminale (Richiede `pip install pytest-cov`):**
Non si indovina la copertura, la si misura. Eseguite questi comandi dalla cartella del progetto:

- **Misurare la Code Coverage:**
  `pytest --cov=nome_del_vostro_file --cov-report=term-missing`
  _Nota:_ Il flag `--cov-report=term-missing` è vitale. Non vi stampa solo una percentuale inutile, ma vi mostra a schermo una colonna "Missing" con il numero di riga esatto delle istruzioni che non sono mai state eseguite dai vostri test.

- **Misurare la Branch Coverage:**
  `pytest --cov=nome_del_vostro_file --cov-branch --cov-report=term-missing`
  _Nota:_ Aggiungendo `--cov-branch`, il tool diventa spietato. Se avete un `if` senza un `else` esplicito e testate solo lo scenario in cui l'`if` è vero, il tool vi segnalerà che il "ramo ombra" (il caso `False`) non è stato coperto (es. leggendo `15->exit` nella colonna Missing).

---

## 2. La Fabbrica dei Dati: Parametrizzazione e nullcontext

Copiare e incollare funzioni di test cambiando solo i valori in ingresso è un errore di design che non supererà mai una Code Review

Nel laboratorio sulle spedizioni (`testing-day3/lab_1_fabbrica/`), abbiamo visto come 5 test identici possano essere distrutti e sostituiti da **una singola matrice dati** tramite il decoratore di parametrizzazione.

Per unire nella stessa matrice i percorsi di successo (Happy Paths) con i percorsi di fallimento (Sad Paths) senza riempire il test di `if` e logica inutile, abbiamo introdotto i Context Manager usando `nullcontext` (importato da `contextlib`).

- **Lo Scudo (`pytest.raises`):** Si usa quando i dati in ingresso devono generare un'eccezione. Assorbe l'urto e fa passare il test.
- **Le Mani Nude (`nullcontext`):** Si usa quando i dati sono validi e non ci si aspetta alcun errore. È un contesto vuoto che lascia fluire l'esecuzione normalmente.

Iniettando lo scudo o il vuoto direttamente dalla matrice dei dati (come visibile in `test_spedizioni_soluzione.py`), otteniamo una singola funzione in grado di governare interamente la logica di business.

---

## 3. Il Problema del Determinismo: Il Mocking

Un test che dipende dalla rete, dall'orologio di sistema o dalla casualità si chiama **Flaky Test** (Test Instabile), fallisce in modo casuale e diventa difficile testare tutti i casi

Per riprendere il controllo totale dell'ambiente, usiamo la libreria `unittest.mock`. Un Mock è un sosia che si sostituisce al componente imprevedibile (come il lancio di un dado nel lab `dado_per_mock`) e restituisce un valore fisso, deterministico, imposto da noi durante la fase di Setup

**⚠️ LA REGOLA D'ORO DEL PATHING:**
Il decoratore di intercettazione non deve mai puntare alla libreria originale globale. **Si intercetta DOVE l'oggetto viene usato**, non dove viene definito.
Se il vostro file `gioco.py` importa e usa il modulo `random`, il path corretto per l'intercettazione sarà `gioco.random.randint`, non semplicemente `random.randint`. Sbagliare questo path significa truccare il componente nella stanza sbagliata.

---

## 4. Documentazione Ufficiale (RTFM)

Usate questi link come riferimento costante durante la risoluzione degli esercizi

- **Pytest Parametrize:** docs.pytest.org/en/stable/how-to/parametrize.html
- **Il Pattern Nullcontext:** docs.python.org/3/library/contextlib.html#contextlib.nullcontext
- **La libreria `unittest.mock`:** docs.python.org/3/library/unittest.mock.html
- **Dove Mockare (Where to patch - FONDAMENTALE):** docs.python.org/3/library/unittest.mock.html#where-to-patch
- **Coverage.py (Misurare la copertura):** coverage.readthedocs.io/
