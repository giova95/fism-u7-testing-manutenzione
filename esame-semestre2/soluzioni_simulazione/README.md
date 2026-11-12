# Soluzioni della simulazione d'esame

**Prima provate da soli**, soprattutto l'Esercizio 2. Poi correggetevi con questa guida e con i file:

| File | Cosa contiene |
|---|---|
| `es1/test_api_biblioteca.py` | Esercizio 1 completo |
| `es2/conftest.py`, `es2/test_prestiti.py`, `es2/test_rete_regionale.py` | Esercizio 2 completo |
| `server_biblioteca.py` | lo stesso server della simulazione |

Per lanciarle: server acceso in un terminale (`python server_biblioteca.py`), poi `cd es1 && pytest -v` (**9 passed**) e `cd ../es2 && pytest -v` (**5 passed**, anche lanciandolo due volte).

All'esame si scrive su carta: contano la logica e il contratto, non la sintassi perfetta.

## 1. Teoria: le 10 risposte

**Chiave: B D A C A D B C A D**

| # | Risp. | Perché è giusta | La trappola nelle altre |
|---|:-----:|-----------------|-------------------------|
| 1 | **B** | Il token è valido, quindi il server **sa chi sei** (autenticazione ok): manca il **permesso** su quella risorsa → `403`. Il `404` è accettabile se non si vuole rivelare che la prenotazione 42 esiste. | **A** `401` = «non so chi sei» (token assente o non valido): qui il token c'è. **C** `500` è sempre un bug del server, mai una risposta voluta. **D** `200` è il bug di sicurezza: Giulia legge i dati di un altro. |
| 2 | **D** | `call_args` registra **come** il mock è stato chiamato: `_, kwargs = mock_get.call_args` e poi `kwargs["timeout"]`. È l'unico modo per verificare un **argomento** passato. | **A** `return_value` è quello che il mock **restituisce**, non quello che riceve. **B** `side_effect = Timeout` simula il guasto, ma il test passerebbe anche se il codice non passasse nessun timeout. **C** falso: il mock lo verifica benissimo. |
| 3 | **A** | `data=` spedisce la stringa **così com'è**, byte per byte, anche se è rotta. L'header `Content-Type: application/json` dice al server di provare a leggerla come JSON → deve rispondere `400`. | **B** `json=` prende un oggetto Python e lo **serializza**: con una stringa spedirebbe `"\"{\\\"username\\\"...\""`, cioè un JSON **valido** (una stringa). **C** il dizionario diventa un JSON corretto: non è più troncato. **D** falso. |
| 4 | **C** | Se il messaggio dice «utente inesistente» per un nome e «password sbagliata» per un altro, un attaccante prova mille nomi e scopre quali sono **veri** (enumerazione degli utenti). Con un messaggio unico non impara niente. | **A**, **B**, **D** sono motivi inventati: il server sa benissimo distinguere i due casi, sceglie di non dirlo. |
| 5 | **A** | Il corriere **risponde**: la chiamata `get` riesce e restituisce una risposta. È `raise_for_status()` della risposta che solleva `HTTPError`. Quindi: risposta finta con `raise_for_status.side_effect = HTTPError(...)`, messa come `return_value` di `get`. | **B** `ConnectionError` è un altro guasto (il corriere non si raggiunge proprio). **C** un `MagicMock` **non** legge lo `status_code`: il suo `raise_for_status()` non fa niente. **D** il mock serve proprio a non spegnere niente. |
| 6 | **D** | Dopo la correzione del Lab 3: corriere guasto → `ServizioSpedizioniNonDisponibile` → l'API risponde `503` con il messaggio, e il carrello **non** viene svuotato (l'utente può riprovare). | **A** `500` era il comportamento **prima** della correzione. **B** il CAP non c'entra. **C** spedire gratis per errore = perdere soldi. |
| 7 | **B** | Un esperimento di chaos parte da un'**ipotesi misurabile**, scritta prima: «503 in meno di 4 secondi, carrello pieno». Così sia verde sia rosso dicono qualcosa. | **A** senza ipotesi non sai se quello che vedi è buono o cattivo. **C** la correzione viene **dopo**, se l'ipotesi è falsa. **D** `sleep` nei test è vietato, e non simula niente. |
| 8 | **C** | Codegen registra **azioni** (click, fill), non **controlli**. Senza `expect(...)` il codice clicca e basta: è verde anche se la pagina mostra un errore. Codegen serve a trovare i locator. | **A** verde senza assert = sempre verde. **B** `sleep` vietato: `expect` aspetta già da solo. **D** un `print` non verifica niente. |
| 9 | **A** | `get_by_label` cerca il **nome** del campo, cioè la `<label>` collegata con `for` all'`id` dell'input. Il placeholder è solo un suggerimento grigio che sparisce quando scrivi: per un lettore di schermo il campo non ha nome. È il primo stop del test d'acquisto fatto in aula. | **B** `sleep` è vietato, e il campo c'è già: non è un problema di tempo, il test aspetta 5 secondi e non lo trova mai. **C** falso. **D** con il server spento il test si ferma prima, sul `goto`. |
| 10 | **D** | Un `<button>` dentro un `<form>` è `submit`: il browser **invia il form e ricarica la pagina**, e con la pagina si perdono il login e il messaggio. Il gestore dell'evento `submit` deve chiamare `evento.preventDefault()`. È la trappola numero 1 del test d'acquisto. | **A** `sleep` vietato, e comunque il messaggio non arriverà mai: la pagina è stata ricaricata. **B** il locator funziona, il bottone viene cliccato. **C** l'`expect` prima del click non cambia cosa succede dopo. |

La 9 e la 10 sono due delle correzioni fatte in aula sull'HTML della Bottega: se le avete sbagliate, rileggete il vostro `index.html` e `app.js`.

## 2. Prima del codice: si legge il contratto

Prima del codice, si legge il **contratto**: ogni riga del contratto è un test.

Le righe da sottolineare:

| Riga del contratto | Cosa diventa nei test |
|---|---|
| «Tutte le risposte sono JSON, errori compresi», «forma `{"errore": "..."}`» | in ogni test d'errore: `assert "errore" in risposta.json()` |
| «**mai** `500` per colpa dell'input» | i body sbagliati devono dare `400`, non `500` (1.4) |
| `GET /api/libri` → «**esattamente** i campi» | `required` con tutti e 4 i campi **e** `additionalProperties: False` (1.1) |
| «inesistente (**anche se `<id>` non è un numero**)» | il caso `"abc"` deve dare `404` (1.2) |
| `POST /api/suggerimenti` → «JSON malformato, body vuoto, non un oggetto, `titolo` non stringa» → `400` | sono **esattamente** i 4 casi della 1.4, nell'ordine |
| utente di test `T-1001` / `4321` | la lacuna (19) |
| `POST /api/reset` → stato iniziale | la lacuna (18) e la `stato_pulito` |
| rete regionale: «entro **2 secondi**» | la lacuna (25): `<= 2` |

Il testo dà quasi tutte le risposte: chi legge con calma il contratto ha già metà dei punti.

## 3. Esercizio 1 (35 punti): black box

**1.1 · Il catalogo rispetta il contratto (lacune 1-8)**

```python
SCHEMA_LIBRO = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "autore": {"type": "string"},                            # (1)
        "disponibile": {"type": "boolean"},                      # (2)
    },
    "required": ["id", "titolo", "autore", "disponibile"],       # (3)
    "additionalProperties": False,
}

def test_catalogo_rispetta_il_contratto():
    risposta = requests.get(f"{BASE_URL}/api/libri", timeout=5)        # (4)
    assert risposta.status_code == 200                                 # (5)
    assert risposta.headers["Content-Type"] == "application/json"      # (6)
    libri = risposta.json()
    assert len(libri) > 0                                              # (7)
    for libro in libri:
        validate(instance=libro, schema=SCHEMA_LIBRO)                  # (8)
```

- (1)-(2): si copia la forma delle righe sopra. In JSON Schema il tipo vero/falso si chiama `boolean`, non `bool` (errore tipico: scrivere il tipo Python).
- (3): `required` è una **lista di stringhe** con i nomi dei campi. Senza, un libro **senza** `autore` passerebbe lo schema. `properties` dice com'è fatto un campo **se c'è**; `required` dice che **deve** esserci.
- (4): l'URL completo, con la f-string e `BASE_URL`.
- (7): `assert libri` funziona, ma `len(libri) > 0` si legge meglio.
- (8): `validate` non restituisce niente: se il libro è sbagliato **solleva** un'eccezione e il test diventa rosso. Quindi niente `assert` davanti (`assert validate(...)` è sempre falso, perché `validate` restituisce `None`: rosso anche quando è giusto).

**1.2 · Libro inesistente, test parametrizzato (lacune 9-11)**

```python
@pytest.mark.parametrize("libro_id", ["999", "0", "abc"])            # (9)
def test_libro_inesistente_risponde_404_in_json(libro_id):
    risposta = requests.get(f"{BASE_URL}/api/libri/{libro_id}", timeout=5)
    assert risposta.status_code == 404                                 # (10)
    assert "errore" in risposta.json()                                 # (11)
```

- (9) è una **lista**: un elemento = un test. `pytest -v` ne mostra tre, con il valore tra parentesi quadre. Vanno bene anche `[999, 0, "abc"]`, tanto finiscono in una f-string.
- (11): il contratto dice «errori in JSON con la chiave `errore`». `"errore" in risposta.json()` controlla la chiave, non il testo del messaggio (che il contratto non fissa).
- Perché proprio `abc`? Perché il contratto lo nomina, e un server fatto male lì risponde `500` (prova a convertirlo in numero e si rompe).

**1.3 · Percorso felice del suggerimento (test da scrivere)**

```python
def test_suggerimento_registrato():
    # Act
    risposta = requests.post(f"{BASE_URL}/api/suggerimenti",
                             json={"titolo": "Dune"}, timeout=5)
    # Assert
    assert risposta.status_code == 201
    assert risposta.json()["titolo"] == "Dune"
```

Qui `json=` va benissimo: il body è un oggetto Python valido. I punti: metodo `post`, `json=` con il dizionario, `timeout`, `201` (non `200`: si è **creato** qualcosa), il titolo letto dalla risposta.

**1.4 · Quattro body non validi (lacune 12-16): il cuore dell'esercizio**

```python
@pytest.mark.parametrize("body_grezzo", [
    '{"titolo": "Dune"',        # JSON troncato
    "",                         # (12) body vuoto
    "[]",                       # (13) JSON valido, ma lista e non oggetto
    '{"titolo": 42}',           # (14) titolo del tipo sbagliato
])
def test_suggerimento_non_valido_risponde_400(body_grezzo):
    risposta = requests.post(
        f"{BASE_URL}/api/suggerimenti",
        data=body_grezzo,                                    # (15)
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    assert risposta.status_code == 400                       # (16)
    assert "errore" in risposta.json()                       # (16)
```

- Ogni caso è una **stringa** Python (lo dice il testo): sono i byte esatti che viaggiano.
- (12): la stringa vuota `""`. Errore tipico: `None` (con `data=None` `requests` non spedisce proprio il body, e il caso diventa un altro).
- (13): `"[]"`. È JSON **valido**: le parentesi quadre sono una lista. Ma il contratto vuole un oggetto, con le graffe. Valido non vuol dire accettabile. Errore tipico: `[]` senza virgolette (è una lista Python, non una stringa).
- (14): `'{"titolo": 42}'`: apici singoli fuori, doppi dentro. Il JSON è perfetto, il **tipo** è sbagliato.
- (15) **risposta aperta**: «`json=` prende un oggetto Python e lo trasforma lui in JSON **corretto**: non può spedire un JSON rotto. A noi serve spedire la stringa **così com'è**, quindi `data=`.» Vale anche: «con `json=` la stringa troncata verrebbe spedita come stringa JSON valida, e il test non proverebbe niente».
- (16): status **e** chiave `errore`. Chi scrive solo lo status prende metà.

## 4. Esercizio 2, Parte A (20 punti): fixture e stato pulito

**2A.1 · `conftest.py` (lacune 17-22)**

```python
@pytest.fixture(autouse=True)                                          # (17)
def stato_pulito(base_url):
    requests.post(f"{base_url}/api/reset", timeout=5)                  # (18)

@pytest.fixture
def token(base_url):
    risposta = requests.post(f"{base_url}/api/login",
                             json={"tessera": "T-1001", "pin": "4321"},   # (19)
                             timeout=5)
    return risposta.json()["token"]                                    # (20)

@pytest.fixture
def auth(token):                                                       # (21)
    return {"Authorization": f"Bearer {token}"}                        # (22)
```

- (17) `autouse=True`: «gira prima di **ogni** test, **senza che nessun test la chieda**». Nello scheletro al PC andava scritto tra le parentesi: `@pytest.fixture(autouse=True)`.
- (18): il contratto: `POST /api/reset`. Errore tipico: `get` al posto di `post` (il server risponde `405`, e lo stato non si pulisce).
- (19): **un dizionario**, con le chiavi del contratto (`tessera`, `pin`, non `username`/`password` della Bottega). Le virgolette su `"4321"`: il contratto dice `str`.
- (20): la risposta è `{"token": "..."}`: si prende `risposta.json()["token"]`. Errore tipico: `return risposta` (si restituisce la risposta intera, non il token).
- (21): una fixture **usa** un'altra fixture mettendola tra i **parametri**: `auth(token)`. Nello scheletro al PC: `LACUNA_21` andava sostituito con `token`.
- (22): un **dizionario** di header, pronto da passare come `headers=auth`. Lo spazio dopo `Bearer` conta.

La catena: `base_url → token → auth`. pytest legge i parametri e costruisce le fixture nell'ordine giusto: voi chiedete `auth`, lui fa prima il login.

**2A.2 · Il prestito (test da scrivere)**

```python
def test_prestito_rende_il_libro_non_disponibile(base_url, auth):
    # Act
    risposta = requests.post(f"{base_url}/api/prestiti",
                             json={"libro_id": 1}, headers=auth, timeout=5)
    # Assert: non mi fido del 201, rileggo lo stato
    assert risposta.status_code == 201
    libro = requests.get(f"{base_url}/api/libri/1", timeout=5).json()
    assert libro["disponibile"] is False
```

- Le fixture si chiedono per **nome** nei parametri: `base_url` e `auth`. La `stato_pulito` **no**: è `autouse`.
- «Rileggendo il libro con una seconda chiamata»: il `201` dice che il server ha **accettato**, la `GET` dimostra che lo stato è **cambiato davvero**.
- «Verde anche dieci volte di fila»: senza reset, al secondo lancio il libro 1 è già in prestito → `409` → rosso. È il motivo dell'`autouse=True` alla (17). Provate: togliete `autouse=True` e lanciate `pytest` due volte.
- `is False` o `== False` vanno entrambi bene; `not libro["disponibile"]` anche.

## 5. Esercizio 2, Parte B (25 punti): il mock della rete regionale

Regola d'oro: **nessun test deve contattare la rete**. Quindi ogni test della Parte B ha un `@patch`.

**2B.1 · Percorso felice (lacune 23-25)**

```python
@patch("rete_regionale.requests.get")                    # (23)
def test_copie_lette_dalla_risposta(mock_get):
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = {"copie": 3}       # (24)
    mock_get.return_value = risposta_finta

    copie = copie_in_rete("9788845292613")

    assert copie == 3
    _, kwargs = mock_get.call_args
    assert kwargs["timeout"] <= 2                         # (25)
```

- (23) la **regola del path**: si patcha **dove viene usato**. `requests.get` è chiamato dentro `rete_regionale.py` → `"rete_regionale.requests.get"`. Errore tipico: `"requests.get"` (in questo caso funziona per caso, ma all'esame la regola vale i punti). Nello scheletro al PC si sostituiva la stringa `"lacuna.LACUNA_23"`.
- (24): `.json` è un **metodo** (si chiama `risposta.json()`), quindi si imposta `json.return_value`. Il valore è un dizionario: `{"copie": 3}`, la stessa forma che il codice legge con `["copie"]`.
- (25): `call_args` = gli argomenti dell'ultima chiamata; `kwargs` sono quelli **con nome** (`timeout=2`). «Al massimo 2 secondi» → `<= 2`. Anche `== 2` è accettabile; l'importante è leggere il `timeout` da `kwargs`.

**2B.2 · Due guasti, un test parametrizzato (test da scrivere)**

```python
@pytest.mark.parametrize("guasto", [
    requests.Timeout("la rete non risponde in tempo"),
    requests.ConnectionError("la rete è irraggiungibile"),
])
@patch("rete_regionale.requests.get")
def test_guasto_di_rete_diventa_errore_di_dominio(mock_get, guasto):
    mock_get.side_effect = guasto          # il mock non risponde: ESPLODE
    with pytest.raises(ReteNonDisponibile):
        copie_in_rete("9788845292613")
```

- «Non risponde in tempo» = `requests.Timeout`; «irraggiungibile» = `requests.ConnectionError`.
- `side_effect` con un'eccezione: chiamare il mock **solleva** l'eccezione, come farebbe `requests` vero.
- `pytest.raises(ReteNonDisponibile)`: il test verifica l'eccezione **di dominio**, non quella di `requests`. Il nostro codice traduce un guasto tecnico in un errore che la biblioteca capisce: il test controlla la traduzione.
- L'ordine dei parametri: prima `mock_get` (da `@patch`, il decoratore più vicino alla funzione), poi `guasto`. Se li invertite, pytest si ferma con `function uses no argument 'guasto'`.
- Errore tipico: due funzioni separate. Funzionano, ma il testo chiede **un'unica** funzione parametrizzata: metà punti.

**2B.3 · La rete risponde 500 (test da scrivere)**

```python
@patch("rete_regionale.requests.get")
def test_rete_risponde_500(mock_get):
    risposta_finta = MagicMock()
    risposta_finta.status_code = 500
    risposta_finta.raise_for_status.side_effect = requests.HTTPError("500")
    mock_get.return_value = risposta_finta

    with pytest.raises(ReteNonDisponibile):
        copie_in_rete("9788845292613")
```

È la domanda 5 della teoria in versione codice. La chiamata **riesce**: `get` restituisce una risposta. È la risposta a dire "500", e `raise_for_status()` la trasforma in eccezione. Errore tipico: solo `status_code = 500` → il `raise_for_status()` del `MagicMock` non fa niente → nessuna eccezione → rosso con `DID NOT RAISE`. Al PC questo errore si vede subito: è il punto più utile da provare.

**2B.4 · L'esperimento (risposte aperte)**

- **a) Ipotesi**, una frase con un numero: «Se la rete regionale è spenta o lenta, `POST /api/richieste-rete` risponde `503` in **meno di 3 secondi**, e il resto della biblioteca (catalogo, prestiti) continua a funzionare.» Punti pieni solo se c'è un numero misurabile.
- **b)** Rete **spenta** → `503` con `{"errore": "rete regionale non disponibile"}`, **subito** (meno di un secondo: la connessione è rifiutata). Rete **lenta (10 s)** → `503` dopo **circa 2 secondi**: il `timeout=2` interrompe l'attesa.
- **c)** Senza `timeout`, il più pericoloso è lo scenario **lento**: con la rete spenta l'errore arriva subito e te ne accorgi; con la rete lenta ogni richiesta resta **appesa** per 10 secondi (o per sempre), l'utente aspetta senza risposta e le richieste bloccate occupano il server, che rallenta anche per chi non usa la rete. È l'esperimento sul corriere della G3: spento → te ne accorgi; lento → blocca tutto.

## 6. Gli errori più frequenti

| Errore | Dove | Correzione |
|---|---|---|
| `bool` al posto di `boolean` nello schema | (2) | i nomi dei tipi sono quelli di JSON Schema |
| `assert validate(...)` | (8) | `validate` non restituisce niente: si chiama e basta |
| `json=` per il body rotto | (15) | `data=` spedisce la stringa così com'è |
| `"[]"` scritto `[]` | (13) | il testo chiede stringhe Python |
| `username`/`password` nel login | (19) | si leggono le chiavi dal contratto: `tessera`/`pin` |
| `return risposta` | (20) | `risposta.json()["token"]` |
| manca `autouse=True` | (17) | il secondo lancio di `test_prestiti` va in `409` |
| `@patch("requests.get")` | (23) | si patcha dove viene usato |
| solo `status_code = 500` | 2B.3 | serve `raise_for_status.side_effect` |
| test senza `assert` | ovunque | verde non vuol dire giusto |
