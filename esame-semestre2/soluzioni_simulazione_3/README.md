# Soluzioni della simulazione 3 (VeloCity)

**Prima provate da soli, con il cronometro.** Poi correggetevi con questa guida e con i file:

| File | Cosa contiene |
|---|---|
| `es1/test_api_velocity.py` | Esercizio 1 completo |
| `es2/conftest.py`, `es2/test_noleggi.py`, `es2/test_sblocco.py` | Esercizio 2 completo |
| `server_velocity.py`, `es2/sblocco.py` | gli stessi della simulazione |

Per lanciarle: `python server_velocity.py` in un terminale, poi `cd es1 && pytest -v` (**9 passed**) e `cd ../es2 && pytest -v` (**5 passed**, anche due volte di fila). I vostri test possono essere scritti in modo diverso: conta che verifichino le stesse cose.

## 1. Teoria

**Chiave: D B A C B D A C D B**

| # | Risp. | Perché | La trappola |
|---|:-----:|--------|-------------|
| 1 | **D** | Il contratto vince sempre: se dice `400` e il server dà `201`, il difetto è del server. Il test rosso ha fatto il suo lavoro. | **C** «adattare il test al server» nasconde il bug: il test non protegge più niente. |
| 2 | **B** | `409` = la richiesta è corretta, ma lo **stato** della risorsa non la permette. | **A** sarebbe `401`, **D** `404`, **C** un `5xx`. |
| 3 | **A** | Senza `additionalProperties: False` lo schema accetta campi in più: il test resta verde anche se il contratto («esattamente») è violato. | `required` controlla solo che i campi **ci siano**. |
| 4 | **C** | Un punto solo da correggere, e ogni test chiede `token` per nome. | **B** è falso: la fixture (scope di default) gira **per ogni test** che la chiede. |
| 5 | **B** | Mockare la funzione da testare = il codice vero non gira mai. Verde, ma non verifica niente: è uno degli errori fatali. | Si mocka quello che la funzione **chiama** (`sblocco.requests.post`), non la funzione. |
| 6 | **D** | `call_args` registra **come** il mock è stato chiamato: qui il body spedito. | **A** confonde quello che si **spedisce** con quello che si **riceve**. |
| 7 | **A** | Spento → errore di connessione subito; lento → `Timeout` dopo i 2 secondi del `timeout`. | **C** è falso: il timeout vale anche per l'attesa della risposta. |
| 8 | **C** | L'esperimento: ipotesi misurabile scritta prima, sistema acceso, servizio esterno guasto davvero, in un ambiente di prova. | **A** è un test con il mock, non un esperimento. **D** non è controllato. |
| 9 | **D** | `get_by_label`: è il **nome** del campo, come lo trova un utente (e un lettore di schermo). | **A**, **B**, **C** dipendono da come è scritto l'HTML, non da cosa vede l'utente. |
| 10 | **B** | La piramide: i casi d'errore sotto, con test API veloci; con il browser pochi flussi importanti. | Test E2E per tutto = suite lenta e fragile. |

## 2. Esercizio 1 (35 punti)

**1.1** — (1) `{"type": "integer"}` · (2) `{"type": "boolean"}` · (3) `["id", "nome", "bici_libere", "attiva"]` · (4) `f"{BASE_URL}/api/stazioni"` · (5) `200` · (6) `"application/json"` · (7) `len(stazioni) > 0` · (8) `validate(instance=stazione, schema=SCHEMA_STAZIONE)`, senza `assert` davanti.

**1.2** — (9) `["999", "0", "centrale"]` · (10) `assert risposta.status_code == 404` · (11) `assert "errore" in risposta.json()`.

**1.3** (scritto per intero):

```python
def test_segnalazione_registrata():
    # Act
    risposta = requests.post(f"{BASE_URL}/api/segnalazioni",
                             json={"stazione_id": 1, "testo": "freno rotto"}, timeout=5)
    # Assert
    assert risposta.status_code == 201
    corpo = risposta.json()
    assert corpo["stazione_id"] == 1
    assert corpo["testo"] == "freno rotto"
    assert isinstance(corpo["id"], int)
```

«Campo per campo»: il contratto dice che il body ha `id`, `stazione_id`, `testo`. L'`id` non lo conosciamo in anticipo: si controlla il **tipo**. Va bene anche validare il body con uno schema.

**1.4** — (12) `'{"stazione_id": 1}'` · (13) `'{"stazione_id": "uno", "testo": "freno rotto"}'` · (14) `'"freno rotto"'` · (15) `data=body_grezzo` · (16) status `400` **e** chiave `errore`.

**Risposta aperta (14):** `"freno rotto"` tra virgolette è una **stringa** JSON valida, ma il contratto vuole un **oggetto** (le graffe) con `stazione_id` e `testo`. Valido non vuol dire accettabile: il server deve rispondere `400`, non `500`.

## 3. Esercizio 2, Parte A (20 punti)

**2A.1** — (17) `autouse=True` · (18) `requests.post(f"{base_url}/api/reset", timeout=5)` · (19) `{"utente": "luca.verdi", "password": "Pedala2026"}` · (20) `risposta.json()["token"]` · (21) `token` · (22) `{"Authorization": f"Bearer {token}"}`.

**2A.2** (scritto per intero):

```python
def test_ultima_bici_noleggiata_poi_409(base_url, auth):
    # Act: noleggio l'unica bici della stazione 2
    risposta = requests.post(f"{base_url}/api/noleggi", json={"stazione_id": 2}, headers=auth, timeout=5)

    # Assert: non mi fido del 201, rileggo la stazione
    assert risposta.status_code == 201
    stazione = requests.get(f"{base_url}/api/stazioni/2", timeout=5).json()
    assert stazione["bici_libere"] == 0

    # Un secondo noleggio alla stessa stazione
    di_nuovo = requests.post(f"{base_url}/api/noleggi", json={"stazione_id": 2}, headers=auth, timeout=5)
    assert di_nuovo.status_code == 409
    assert "errore" in di_nuovo.json()
```

Le fixture si chiedono per nome (`base_url`, `auth`); la `stato_pulito` no, è `autouse`. Senza `autouse`, al secondo lancio il **primo** noleggio risponde già `409` e il test diventa rosso.

## 4. Esercizio 2, Parte B (25 punti)

**2B.1** — (23) `"sblocco.requests.post"` · (24) `{"sbloccata": True}` · (25) `kwargs["timeout"] <= 2` · (26) `kwargs["json"]["stazione_id"] == 2`: il body spedito è nell'argomento con nome `json`.

**2B.2** (scritto per intero):

```python
@pytest.mark.parametrize("guasto", [
    requests.Timeout("SbloccoBici non risponde in tempo"),
    requests.ConnectionError("SbloccoBici irraggiungibile"),
])
@patch("sblocco.requests.post")
def test_guasto_diventa_errore_di_dominio(mock_post, guasto):
    mock_post.side_effect = guasto
    with pytest.raises(SbloccoNonDisponibile):
        sblocca(2, "luca.verdi")
```

Prima `mock_post` (dal `@patch`, il decoratore più vicino alla funzione), poi `guasto`: invertiti, pytest si ferma con `function uses no argument 'guasto'`. Due funzioni separate funzionano, ma il testo chiede **un'unica** funzione parametrizzata.

**2B.3** (scritto per intero):

```python
@patch("sblocco.requests.post")
def test_sbloccobici_risponde_500(mock_post):
    risposta_finta = MagicMock()
    risposta_finta.status_code = 500
    risposta_finta.raise_for_status.side_effect = requests.HTTPError("500")
    mock_post.return_value = risposta_finta
    with pytest.raises(SbloccoNonDisponibile):
        sblocca(2, "luca.verdi")
```

**2B.4**
- **a)** «Se SbloccoBici è spento o lento, `POST /api/noleggi` risponde `503` in **meno di 3 secondi**, e la bici resta libera.»
- **b)** Spento → `503` **subito**. Lento 10 s → `503` dopo **circa 2 secondi**, il timeout.
- **c)** Il test con il mock verifica **la nostra funzione** da sola: che traduca il guasto in `SbloccoNonDisponibile`. L'esperimento verifica **il sistema intero acceso**: che il server catturi l'eccezione, risponda `503` all'utente, nei tempi giusti, senza lasciare la bici occupata. Servono tutti e due.

## 5. Gli errori più frequenti

| Errore | Dove | Correzione |
|---|---|---|
| `'freno rotto'` senza virgolette doppie dentro | (14) | il JSON di una stringa ha le virgolette doppie: `'"freno rotto"'` |
| `assert risposta.json() == {...}` con l'`id` scritto a mano | 1.3 | l'`id` non si conosce: si controlla il tipo |
| `username` al posto di `utente` nel login | (19) | le chiavi si leggono dal contratto |
| solo il primo noleggio, senza rileggere la stazione | 2A.2 | il `201` non basta: si rilegge lo stato |
| `@patch("sblocco.sblocca")` | 2B | mocka la funzione da testare: errore fatale |
| solo `status_code = 500` | 2B.3 | serve `raise_for_status.side_effect` |
