# Soluzioni della simulazione 2 (Cinema Aurora)

**Prima provate da soli.** Poi correggetevi con questa guida e con i file:

| File | Cosa contiene |
|---|---|
| `es1/test_api_cinema.py` | Esercizio 1 completo |
| `es2/conftest.py`, `es2/test_biglietti.py`, `es2/test_pagamenti.py` | Esercizio 2 completo |
| `server_cinema.py`, `es2/pagamenti.py` | gli stessi della simulazione |

Per lanciarle: `python server_cinema.py` in un terminale, poi `cd es1 && pytest -v` (**9 passed**) e `cd ../es2 && pytest -v` (**5 passed**, anche due volte di fila).

## 1. Teoria

**Chiave: C A D B C A D B A C**

| # | Risp. | Perché | La trappola |
|---|:-----:|--------|-------------|
| 1 | **C** | `201 Created` = è nata una risorsa nuova. Il contratto lo dice, e il test controlla il contratto. | `200` è il "va bene" generico: se il contratto dice 201, un 200 è un difetto. |
| 2 | **A** | Senza token il server **non sa chi siete**: `401`. | `403` è per chi è riconosciuto ma non ha il permesso. |
| 3 | **D** | pytest legge i parametri delle fixture e costruisce la catena da solo: `base_url → token → auth`. | Le fixture non si chiamano mai a mano. |
| 4 | **B** | Regola del path: si patcha **dove viene usato**, nel modulo `pagamenti`. | **C** mocka la funzione da testare: il test è verde ma non verifica niente (errore fatale). |
| 5 | **C** | `side_effect` con un'eccezione fa **esplodere** la chiamata, come farebbe `requests` vero. | **A** fa **restituire** l'eccezione come se fosse una risposta: nessuno la solleva. |
| 6 | **A** | `additionalProperties: False` vieta i campi non elencati: «esattamente» vuol dire anche "niente di più". | `required` dice cosa **deve** esserci, non cosa è vietato. |
| 7 | **D** | Lo stato del server sopravvive tra i test: serve il reset prima di **ogni** test, con `autouse`. | **C** indebolisce il test finché non verifica più niente. |
| 8 | **B** | Ruolo + nome: è come un utente (e un lettore di schermo) trova il bottone. Non dipende dalla grafica. | **A** e **C** si rompono appena cambia l'impaginazione. |
| 9 | **A** | La piramide: tanti test veloci in basso (API, mock), pochi E2E in cima per i flussi importanti. | I test con il browser sono lenti e fragili: 15 casi lì costano minuti a ogni push. |
| 10 | **C** | Ci sono 4 bottoni "Aggiungi", uno per scheda: si sceglie prima la scheda giusta, poi il bottone dentro. | **B** prende il primo a caso: il test compra il prodotto sbagliato senza accorgersene. |

## 2. Esercizio 1 (35 punti)

**1.1** — (1) `{"type": "integer"}` · (2) `{"type": "boolean"}` (il nome JSON Schema, non `bool`) · (3) `["id", "titolo", "durata", "in_sala"]` · (4) `f"{BASE_URL}/api/film"` · (5) `200` · (6) `"application/json"` · (7) `len(film) > 0` · (8) `validate(instance=un_film, schema=SCHEMA_FILM)`, senza `assert` davanti: `validate` non restituisce niente, solleva un'eccezione se il film è sbagliato.

**1.2** — (9) `["999", "-1", "xyz"]`, una lista: un elemento = un test · (10) `assert risposta.status_code == 404` · (11) `assert "errore" in risposta.json()`. Perché `-1` e `xyz`? Il contratto dice «anche se non è un numero intero positivo»: un server fatto male lì risponde `500`.

**1.3** — (12) `json={"film_id": 1, "voto": 5}`: qui `json=` va bene, il body è un dizionario valido · (13) `201` · (14) `risposta.json() == {"film_id": 1, "voto": 5}`: il contratto dice «uguale a quello inviato», quindi si confronta il body intero.

**1.4** — (15) `""` · (16) `'{"film_id": 1}'` (JSON perfetto, ma manca un campo) · (17) `'{"film_id": 1, "voto": "cinque"}'` (apici singoli fuori, doppi dentro) · (18) `data=body_grezzo` · (19) `assert risposta.status_code == 400` **e** `assert "errore" in risposta.json()`.

**Risposta aperta (18):** `json=` prende un oggetto Python e lo trasforma in JSON **corretto**: non può spedire un JSON rotto o vuoto. Per spedire la stringa così com'è serve `data=`.

## 3. Esercizio 2, Parte A (20 punti)

**2A.1** — (20) `autouse=True` · (21) `requests.post(f"{base_url}/api/reset", timeout=5)` (POST, non GET) · (22) `{"email": "anna@aurora.it", "password": "Popcorn24"}`: le chiavi si leggono dal contratto · (23) `risposta.json()["token"]` · (24) `token` · (25) `{"Authorization": f"Bearer {token}"}`, con lo spazio dopo `Bearer`.

**2A.2** — (26) `{"proiezione_id": 1}` · (27) `auth` (la fixture è già l'header pronto) · (28) `f"{base_url}/api/proiezioni/1"` · (29) `proiezione["posti_liberi"] == 49`.

Il `201` dice che il server ha **accettato**; la seconda chiamata dimostra che lo stato è **cambiato davvero**. «Verde dieci volte di fila»: senza `autouse`, al secondo lancio i posti sono 48 e il test diventa rosso. Provate: togliete `autouse=True` e lanciate due volte.

## 4. Esercizio 2, Parte B (25 punti)

**2B.1** — (30) `"pagamenti.requests.post"`: il client usa `post`, e si patcha dove viene usato · (31) `{"transazione": "TX-42"}`, la forma che il codice legge con `["transazione"]` · (32) `kwargs["timeout"] <= 3`.

**2B.2** — (33) `[requests.Timeout("..."), requests.ConnectionError("...")]` · (34) `mock_post.side_effect = guasto` · (35) `pytest.raises(PagamentoNonDisponibile)`: si verifica l'eccezione **di dominio**, non quella di `requests`. Il nostro codice traduce un guasto tecnico in un errore che il cinema capisce: il test controlla la traduzione.

**2B.3** — (36) `risposta_finta.raise_for_status.side_effect = requests.HTTPError("503")` · (37) `mock_post.return_value = risposta_finta`. La chiamata **riesce**: è la risposta a dire "503", e `raise_for_status()` la trasforma in eccezione. Solo `status_code = 503` non basta: il `raise_for_status()` di un `MagicMock` non fa niente, e il test finisce con `DID NOT RAISE`.

**2B.4**
- **a)** «Se PagaSicuro è spento o lento, `POST /api/biglietti` risponde `503` in **meno di 4 secondi**, e il posto resta libero.» Serve un numero misurabile.
- **b)** Spento → `503` **subito** (la connessione è rifiutata). Lento 10 s → `503` dopo **circa 3 secondi**, il timeout.
- **c)** `GET /api/proiezioni/1` dopo il `503`: `posti_liberi` deve essere **ancora 50**. È la stessa idea della 2A.2: non ci si fida dello status, si rilegge lo stato.

## 5. Gli errori più frequenti

| Errore | Dove | Correzione |
|---|---|---|
| `bool` al posto di `boolean` | (2) | i tipi sono quelli di JSON Schema |
| `assert validate(...)` | (8) | `validate` si chiama e basta |
| `json=` per il body rotto | (18) | `data=` spedisce la stringa così com'è |
| `GET` sul reset | (21) | il contratto dice `POST /api/reset` |
| `return risposta` | (23) | `risposta.json()["token"]` |
| `@patch("pagamenti.requests.get")` | (30) | il client usa `post`: si patcha quello che viene **chiamato** |
| solo `status_code = 503` | (36) | serve `raise_for_status.side_effect` |
