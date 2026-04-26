# Regole per il test di fine modulo

## Parametri della Prova

- **Tempo a disposizione:** 120 Minuti(30 per la teoria, 90 per la parte pratica)
- **Punteggio Totale:** 100 Punti
- **Soglia di Superamento:** 60/100.
- **Modalità:** Cartaceo (Niente PC, niente IDE, niente Smartphone)

## Regole

L'obiettivo di questo esame non è valutare se sapete scrivere codice a memoria, ma se sapete progettare un'architettura di testing resiliente

1. **Nessun aiuto esterno:** È vietato l'uso di smartphone o documentazione non fornita dal docente
2. **Sintassi vs Logica:** Siete valutati sulla logica (isolamento, mock pathing corretto, asserzioni sensate, standard POSIX). Piccoli errori veniali di sintassi Python (es. dimenticare i due punti `:` a fine riga o un indentazione imperfetta) non causeranno l'annullamento dell'esercizio, purché il design del test sia corretto
3. **Cheat Sheet:** Avete a disposizione un foglio di supporto sintattico. Nella cartella trovate il pdf stampabile e il markdown (Uno sviluppatore non impara a memoria, sa dove cercare le informazioni)

## Struttura dell'Esame

### PARTE 1: Teoria Architetturale e Sistemistica (20 Punti | Tempo: 30 Minuti)

- **10 Domande a risposta multipla** (2 punti ciascuna)
- **Argomenti:** Git Flow, CI/CD (GitHub Actions), Metriche di Coverage, Fondamenti di Mocking, Standard POSIX, Teoria del Black/White Box Testing.
- **Esecuzione:** Una sola risposta è corretta. Leggete attentamente

### PARTE 2: Ingegneria Pratica (80 Punti | Tempo: 90 Minuti)

- **3 Esercizi di stesura codice su foglio**
- **Livello 1 (20 Punti) - White Box Base:** Stesura di test applicando il pattern Arrange-Act-Assert e gestendo le eccezioni
- **Livello 2 (30 Punti) - Parametrizzazione e Mocking:** Creazione di un singolo test parametrizzato per governare più scenari e utilizzo del decoratore `@patch`
- **Livello 3 (30 Punti) - Black Box CLI Testing:** Utilizzo della libreria `subprocess` per invocare un programma esterno come scatola nera, verificando la correttezza del payload testuale e degli Exit Code

### SIMULAZIONI DEL TEST

Trovate inoltre nella cartella due markdown: due simulazioni della parte teorica e una per la parte pratica
