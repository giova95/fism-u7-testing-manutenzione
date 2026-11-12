# SIMULAZIONE 2 (guidata): Parte Pratica (90 minuti, 80 punti)

Stessa struttura dell'esame, contesto diverso. Questa simulazione è **guidata**: quasi tutto è a lacune, come l'esame vero.

- **Al PC** (consigliato a casa): il codice è nelle cartelle `es1/` e `es2/` qui accanto, dove ogni lacuna `__(7)__` del testo è scritta `LACUNA(7)`. Istruzioni nel [`README.md`](README.md).
- **Su carta** (come all'esame): sul foglio scrivete il numero della lacuna e quello che va al suo posto, per esempio «(7) len(film) > 0».

Pattern Arrange-Act-Assert; ogni chiamata di rete ha un `timeout`. Se una parola non vi è chiara, la trovate in [`CONCETTI_BASE.md`](../../CONCETTI_BASE.md).

## Il contesto: il Cinema Aurora

Il backend del cinema espone un'API REST su `http://localhost:8000`. Il riferimento è **il contratto** qui sotto, non il codice del server: siete una scatola nera.

**Il contratto dell'API**

- Tutte le risposte sono JSON (`Content-Type: application/json`), errori compresi. Ogni errore ha la forma `{"errore": "..."}`. Il server non risponde **mai** `500` a causa dell'input del client.
- `GET /api/film` → `200`, body: lista dei film. Ogni film ha **esattamente** i campi `{"id": int, "titolo": str, "durata": int, "in_sala": bool}`.
- `GET /api/film/<id>` → `200` con il film. Film inesistente (anche se `<id>` non è un numero intero positivo) → `404` con `{"errore": "..."}`.
- `POST /api/recensioni` (pubblico), body `{"film_id": int, "voto": int}` → `201`, body `{"film_id": int, "voto": int}`, uguale a quello inviato. Film inesistente → `404`. Body non valido (JSON malformato, body vuoto, campo mancante, tipo sbagliato) → `400`.
- `POST /api/login`, body `{"email": str, "password": str}` → `200`, body `{"token": str}`; credenziali errate → `401`. Utente di test: `anna@aurora.it` / `Popcorn24`.
- `GET /api/proiezioni/<id>` → `200`, body `{"id": int, "film_id": int, "posti_liberi": int}`.
- `POST /api/biglietti` (header `Authorization: Bearer <token>`), body `{"proiezione_id": int}` → `201`, body `{"id": int, "proiezione_id": int}`; posti esauriti → `409`. Prima di emettere il biglietto, il cinema addebita il prezzo con **PagaSicuro**, un servizio esterno: se PagaSicuro non risponde entro 3 secondi, o risponde con un errore → `503` con `{"errore": "servizio pagamenti non disponibile"}`. Nell'ambiente di test PagaSicuro approva sempre.
- `POST /api/reset` → `200`. Solo in ambiente di test: riporta i dati allo stato iniziale (proiezione 1 con 50 posti liberi, proiezione 2 con 1 posto libero, nessun biglietto).

## ESERCIZIO 1: Black Box di un'API REST (35 Punti)

File `test_api_cinema.py`, con la libreria `requests`.

**1.1 (10 punti)** `GET /api/film`: status, formato, lista non vuota, e **ogni** film rispetta lo schema del contratto.

```python
import pytest
import requests
from jsonschema import validate

BASE_URL = "http://localhost:8000"

SCHEMA_FILM = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "durata": __(1)__,
        "in_sala": __(2)__,
    },
    "required": __(3)__,
    "additionalProperties": False,
}


def test_programmazione_rispetta_il_contratto():
    # Act
    risposta = requests.get(__(4)__, timeout=5)

    # Assert
    assert risposta.status_code == __(5)__
    assert risposta.headers["Content-Type"] == __(6)__
    film = risposta.json()
    assert __(7)__                   # la lista non è vuota
    for un_film in film:
        __(8)__                      # il film rispetta SCHEMA_FILM
```

**1.2 (6 punti)** Un **unico** test parametrizzato verifica che i film `999`, `-1` e `xyz` rispondano come dice il contratto per un film inesistente.

```python
@pytest.mark.parametrize("film_id", __(9)__)
def test_film_inesistente_risponde_404_in_json(film_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/film/{film_id}", timeout=5)

    # Assert
    __(10)__                         # lo status code
    __(11)__                         # la chiave "errore" nel body
```

**1.3 (6 punti)** Il percorso felice di `POST /api/recensioni`: voto `5` al film `1`.

```python
def test_recensione_registrata():
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        __(12)__,                    # il body: voto 5 al film 1
        timeout=5,
    )

    # Assert
    assert risposta.status_code == __(13)__
    assert __(14)__                  # il body della risposta è quello del contratto
```

**1.4 (13 punti)** Un **unico** test parametrizzato verifica che `POST /api/recensioni` risponda come dice il contratto a quattro body non validi. Ogni lacuna dei casi è una **stringa** Python.

```python
@pytest.mark.parametrize("body_grezzo", [
    '{"film_id": 1, "voto": 5',        # JSON troncato (questo è già scritto)
    __(15)__,                        # body vuoto
    __(16)__,                        # manca il campo "voto"
    __(17)__,                        # il voto è del tipo sbagliato
])
def test_recensione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/recensioni",
        __(18)__,                    # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    __(19)__                         # una o due righe: status e chiave "errore"
```

Domanda (lacuna 18): perché qui non si può usare `json=`? Rispondete in una o due righe.

## ESERCIZIO 2: Fixture, stato pulito e servizi esterni (45 Punti)

**Parte A (20 punti).**

**2A.1 (12 punti)** Completate `conftest.py`.

```python
# conftest.py
import pytest
import requests

@pytest.fixture
def base_url():
    return "http://localhost:8000"


@pytest.fixture(__(20)__)                      # deve girare prima di OGNI test, senza che nessun test la chieda
def stato_pulito(base_url):
    __(21)__                         # riporta il server allo stato iniziale


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json=__(22)__,
        timeout=5,
    )
    return __(23)__


@pytest.fixture
def auth(__(24)__):                   # auth USA un'altra fixture: quale?
    return __(25)__                  # l'header di autenticazione pronto all'uso
```

**2A.2 (8 punti)** Completate `test_biglietti.py`: il test compra un biglietto per la proiezione `1` e poi verifica, **rileggendo la proiezione con una seconda chiamata**, che i posti liberi siano scesi di uno. Il test deve restare verde anche lanciando `pytest` dieci volte di fila.

```python
def test_biglietto_occupa_un_posto(base_url, auth):
    # Act
    risposta = requests.post(
        f"{base_url}/api/biglietti",
        json=__(26)__,               # un biglietto per la proiezione 1
        headers=__(27)__,
        timeout=5,
    )

    # Assert: non mi fido del 201, rileggo lo stato
    assert risposta.status_code == 201
    proiezione = requests.get(__(28)__, timeout=5).json()
    assert __(29)__                  # all'inizio i posti liberi sono 50
```

**Parte B (25 punti).** Il client di PagaSicuro è `pagamenti.py`:

```python
# pagamenti.py — client di PagaSicuro (servizio esterno di pagamento, NON è nostro)
import requests

PAGASICURO_URL = "https://api.pagasicuro.example/v1"


class PagamentoNonDisponibile(Exception):
    """PagaSicuro non risponde o risponde male: errore di DOMINIO, non di rete."""


def addebita(importo: float) -> str:
    """Addebita l'importo del biglietto e restituisce il codice della transazione."""
    try:
        risposta = requests.post(f"{PAGASICURO_URL}/addebiti", json={"importo": importo}, timeout=3)
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise PagamentoNonDisponibile(str(errore)) from errore
    return risposta.json()["transazione"]
```

I test vanno in `test_pagamenti.py`. **Nessun test deve contattare PagaSicuro.** Attenzione: questa volta il client usa `requests.post`, non `requests.get`.

```python
# test_pagamenti.py
from unittest.mock import MagicMock, patch

import pytest
import requests

from pagamenti import PagamentoNonDisponibile, addebita
```

**2B.1 (7 punti)** Il percorso felice: PagaSicuro risponde `{"transazione": "TX-42"}`, la funzione restituisce `"TX-42"` e la chiamata è stata fatta con un `timeout` di al massimo 3 secondi.

```python
@patch(__(30)__)             # Regola del path: dove viene USATO
def test_addebito_restituisce_la_transazione(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = __(31)__      # PagaSicuro risponde con la transazione "TX-42"
    mock_post.return_value = risposta_finta

    # Act
    codice = addebita(9.5)

    # Assert
    assert codice == "TX-42"
    _, kwargs = mock_post.call_args
    assert __(32)__                  # timeout di al massimo 3 secondi
```

**2B.2 (8 punti)** Un **unico** test parametrizzato simula sia PagaSicuro che **non risponde in tempo** sia PagaSicuro **irraggiungibile**: in entrambi i casi deve essere sollevata `PagamentoNonDisponibile`. Alla lacuna (33) va la lista dei due guasti.

```python
@pytest.mark.parametrize("guasto", __(33)__)         # PagaSicuro non risponde in tempo / è irraggiungibile
@patch("pagamenti.requests.post")
def test_guasto_diventa_errore_di_dominio(mock_post, guasto):
    # Arrange
    __(34)__                         # il mock non risponde: ESPLODE con il guasto

    # Act + Assert
    with __(35)__:                   # ci aspettiamo l'eccezione di DOMINIO
        addebita(9.5)
```

**2B.3 (5 punti)** PagaSicuro **risponde**, ma con lo status `503`: anche in questo caso deve essere sollevata `PagamentoNonDisponibile`.

```python
@patch("pagamenti.requests.post")
def test_pagasicuro_risponde_503(mock_post):
    # Arrange: la chiamata RIESCE, è la risposta a contenere l'errore
    risposta_finta = MagicMock()
    risposta_finta.status_code = 503
    __(36)__                         # raise_for_status() della risposta finta deve sollevare HTTPError
    __(37)__                         # il mock restituisce la risposta finta

    # Act + Assert
    with pytest.raises(PagamentoNonDisponibile):
        addebita(9.5)
```

**2B.4 (5 punti)** I test con il mock sono verdi. Ora volete sapere se **il cinema intero** regge quando PagaSicuro si guasta, con un esperimento come quello fatto in aula con il corriere della Bottega.

a) Scrivete l'**ipotesi** dell'esperimento, in una frase, con un numero che si possa misurare.

b) Con PagaSicuro **spento**, cosa si aspetta l'utente da `POST /api/biglietti` (status code e tempo massimo di risposta)? E con PagaSicuro **lento** (10 secondi)?

c) Dopo il `503`, il posto **non** deve risultare occupato. Con quale chiamata lo verificate, e cosa vi aspettate di leggere?
