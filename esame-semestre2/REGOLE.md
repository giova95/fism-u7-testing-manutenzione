# Regole per il test di fine modulo (Semestre 2)

## Parametri della Prova

- **Data:** Mercoledì 25/11/2026, prima parte della mattina
- **Tempo a disposizione:** 120 Minuti (30 per la teoria, 90 per la parte pratica)
- **Punteggio Totale:** 100 Punti
- **Soglia di Superamento:** 60/100
- **Modalità:** Cartaceo (Niente PC, niente IDE, niente Smartphone)

## Regole

L'obiettivo di questo esame non è valutare se sapete scrivere codice a memoria, ma se sapete progettare dei test di cui ci si può fidare. Come nel semestre 1, ma su un sistema distribuito: un server raggiungibile solo via rete e un servizio esterno che può guastarsi. All'esame c'è **solo quello che abbiamo fatto in aula**: la parte pratica riguarda le API, le fixture e i mock, come nei lab corretti insieme in aula.

1. **Nessun aiuto esterno:** È vietato l'uso di smartphone o documentazione non fornita dal docente
2. **Sintassi vs Logica:** Siete valutati sulla logica (scatola nera, isolamento, stato pulito, path corretto del mock, asserzioni sul contratto, gestione dei guasti). Piccoli errori veniali di sintassi Python (es. dimenticare i due punti `:` a fine riga, un'indentazione imperfetta, una virgola mancante) non causeranno l'annullamento dell'esercizio, purché il design del test sia corretto
3. **Cheat Sheet:** Avete a disposizione un foglio di supporto sintattico. Nella cartella trovate il pdf stampabile e il markdown (Uno sviluppatore non impara a memoria, sa dove cercare le informazioni). Vi dice **come** si scrive una cosa, non **quando** usarla
4. **Il contratto vince sempre:** negli esercizi sulle API il riferimento è la specifica stampata nel testo, non quello che "secondo voi" dovrebbe fare il server

## Quality Gate: gli errori fatali

In azienda certi errori non sono "mezzo punto in meno": sono test che danno una falsa sicurezza, e una falsa sicurezza è peggio di nessun test. Per questo alcuni errori **azzerano il punto (o l'esercizio) in cui compaiono**, indipendentemente da quanto è bello il resto del codice:

- **Scatola nera violata:** nei test di un'API importare il codice del server (`from app import ...`) invece di parlarci via HTTP
- **Mock che non isola:** un test che fa partire una chiamata di rete vera verso un servizio esterno, oppure che mocka **la funzione stessa** che dovrebbe testare (il test diventa verde, ma non verifica niente)
- **Test dipendenti dall'ordine:** test che passano solo se eseguiti in una certa sequenza, o solo la prima volta, perché lo stato del server non viene riportato a una condizione nota
- **`sleep` per "aspettare":** usare `time.sleep()` in un test per sincronizzarsi con un server o per simulare un servizio lento, invece del `timeout` e dei mock. Vale anche nei test con il browser: `time.sleep()` o `wait_for_timeout()` al posto di `expect(...)`

Errori **veniali** (tolgono pochi punti, non azzerano): sintassi, una chiamata senza `timeout`, nomi poco chiari, commenti AAA mancanti.

## Struttura dell'Esame

### PARTE 1: Teoria (20 Punti | Tempo: 30 Minuti)

- **10 Domande a risposta multipla** (2 punti ciascuna, 4 opzioni)
- **Argomenti:** quasi tutte le domande sono su quello che abbiamo fatto con le API: status code e contratto, stato pulito e test isolati, fixture, mock e iniezione di guasti, eccezioni di dominio, l'esperimento sul corriere. Poche domande di base (al massimo tre) sui test con il browser (Playwright) e sulla piramide dei test
- **Esecuzione:** Una sola risposta è corretta. Leggete attentamente

### PARTE 2: Pratica (80 Punti | Tempo: 90 Minuti)

- **2 Esercizi su foglio**, con il **contratto stampato** nel testo. Molte parti sono **scheletri da completare**: ogni lacuna ha un numero (`__(7)__`) e sul foglio scrivete il numero e quello che va al suo posto. Alcuni test li scrivete per intero, sul modello degli scheletri
- **Esercizio 1 (35 Punti) - Black Box di un'API REST:** test con `requests` su un contratto dato: status code, `Content-Type`, schema del JSON con `jsonschema`, risorsa inesistente (404 in JSON), payload corrotti in un test parametrizzato (`data=`)
- **Esercizio 2 (45 Punti) - Fixture, stato pulito e servizi esterni:** `conftest.py` con la catena di fixture (login → token → header) e lo stato pulito `autouse`, un test che verifica lo stato con una seconda chiamata; mock di un servizio esterno con iniezione di guasti (timeout, server irraggiungibile, risposta 503) ed eccezione di dominio; una domanda aperta sull'esperimento con il servizio esterno spento o lento

### SIMULAZIONI DEL TEST

Tre simulazioni, con la stessa struttura dell'esame e contesti diversi. Ognuna ha un server da avviare e il codice da completare al PC, oltre al testo per lavorare su carta come all'esame.

| Simulazione | Livello | Dove | Soluzioni |
|---|---|---|---|
| 1. La Biblioteca civica | come l'esame | fatta in aula l'11/11: [`simulazione_pc/`](simulazione_pc/README.md) | già pubblicate: [`soluzioni_simulazione/`](soluzioni_simulazione/README.md) |
| 2. Il Cinema Aurora | **guidata**: quasi tutto a lacune | a casa: [`simulazione_2/`](simulazione_2/README.md) | mercoledì 18/11 |
| 3. VeloCity | **come l'esame**: alcuni test da scrivere per intero | a casa, dopo la 2: [`simulazione_3/`](simulazione_3/README.md) | mercoledì 18/11 |

Fatele con il cronometro (30 minuti di teoria, 90 di pratica) e con il solo cheat sheet. Segnate i dubbi: li riprendiamo il 25/11 prima dell'esame.
