# SIMULAZIONE DI ESAME: Parte Pratica (90 minuti, 80 punti)

> 💻 **Mercoledì 11/11 la facciamo al PC:** il codice da completare è nella cartella [`simulazione_pc/`](simulazione_pc/README.md), dove ogni lacuna `__(7)__` del testo è scritta `LACUNA(7)`. All'esame del 25/11 si lavora invece su carta, come descritto qui sotto.

Stessa struttura dell'esame vero, contesto diverso. Lavorate sul foglio protocollo, indicando sempre il nome del file. Negli scheletri ogni lacuna ha un numero, per esempio `__(7)__`: sul foglio scrivete il numero e quello che va al suo posto («(7) len(libri) > 0»). Dove il testo dice «scrivete il test», scrivete la funzione intera. Pattern Arrange-Act-Assert; ogni chiamata di rete ha un `timeout`.

> 📖 Se una parola non vi è chiara (status code, JSON, header, token, fixture, mock, timeout), la trovate in [`CONCETTI_BASE.md`](../CONCETTI_BASE.md). Gli esempi da cui partire sono nei lab della G1 (`testing-day6/`) e nel cheat sheet.

## Il contesto: la Biblioteca civica

Il backend della biblioteca espone un'API REST su `http://localhost:8000`. Il riferimento è **il contratto** qui sotto, non il codice del server: siete una scatola nera.

**Il contratto dell'API**

- Tutte le risposte sono JSON, errori compresi. Ogni errore ha la forma `{"errore": "..."}`. Il server non risponde **mai** `500` a causa dell'input del client.
- `GET /api/libri` → `200`, body: lista di libri. Ogni libro ha **esattamente** i campi `{"id": int, "titolo": str, "autore": str, "disponibile": bool}`.
- `GET /api/libri/<id>` → `200` con il libro. Libro inesistente (anche se `<id>` non è un numero) → `404` con `{"errore": "..."}`.
- `POST /api/suggerimenti` (pubblico), body `{"titolo": str}` → `201`, body `{"titolo": str}`. Body non valido (JSON malformato, body vuoto, JSON che non è un oggetto, `titolo` non stringa) → `400`.
- `POST /api/login`, body `{"tessera": str, "pin": str}` → `200`, body `{"token": str}`; credenziali errate → `401`. Utente di test: tessera `T-1001`, pin `4321`.
- `POST /api/prestiti` (header `Authorization: Bearer <token>`), body `{"libro_id": int}` → `201`; libro già in prestito → `409`.
- `POST /api/richieste-rete` (header `Authorization: Bearer <token>`), body `{"isbn": str}` → `201`. Chiede il libro alle altre biblioteche della **Rete Bibliotecaria Regionale**, un servizio esterno: se la rete non risponde entro 2 secondi, o risponde con un errore → `503` con `{"errore": "rete regionale non disponibile"}`.
- `POST /api/reset` → `200`. Solo in ambiente di test: riporta i dati allo stato iniziale (libri 1 e 2 disponibili).

## ESERCIZIO 1: Black Box di un'API REST (35 Punti)

File `test_api_biblioteca.py`, con la libreria `requests`.

**1.1 (10 punti)** Completate lo scheletro: `GET /api/libri` (status, formato, lista non vuota) e **ogni** libro rispetta lo schema del contratto.

```python
import pytest
import requests
from jsonschema import validate

BASE_URL = "http://localhost:8000"

SCHEMA_LIBRO = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "titolo": {"type": "string"},
        "autore": __(1)__,
        "disponibile": __(2)__,
    },
    "required": __(3)__,
    "additionalProperties": False,
}


def test_catalogo_rispetta_il_contratto():
    # Act
    risposta = requests.get(__(4)__, timeout=5)

    # Assert
    assert risposta.status_code == __(5)__
    assert risposta.headers["Content-Type"] == __(6)__
    libri = risposta.json()
    assert __(7)__                     # la lista non è vuota
    for libro in libri:
        __(8)__                        # il libro rispetta SCHEMA_LIBRO
```

**1.2 (6 punti)** Completate lo scheletro: un **unico** test parametrizzato verifica che i libri `999`, `0` e `abc` rispondano come dice il contratto per un libro inesistente.

```python
@pytest.mark.parametrize("libro_id", __(9)__)
def test_libro_inesistente_risponde_404_in_json(libro_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/libri/{libro_id}", timeout=5)

    # Assert
    __(10)__                           # lo status code
    __(11)__                           # la chiave "errore" nel body
```

**1.3 (6 punti)** Scrivete il test del percorso felice di `POST /api/suggerimenti` con il titolo «Dune»: verificate lo status e che il body restituito contenga il titolo inviato.

**1.4 (13 punti)** Completate lo scheletro: un **unico** test parametrizzato verifica che `POST /api/suggerimenti` risponda come dice il contratto a quattro body non validi. Ogni lacuna dei casi è una **stringa** Python.

```python
@pytest.mark.parametrize("body_grezzo", [
    '{"titolo": "Dune"',                 # JSON troncato (questo è già scritto)
    __(12)__,                            # body vuoto
    __(13)__,                            # JSON valido, ma è una lista e non un oggetto
    __(14)__,                            # titolo del tipo sbagliato
])
def test_suggerimento_non_valido_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/suggerimenti",
        __(15)__,                        # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    __(16)__                             # una o due righe: status e chiave "errore"
```

Domanda (lacuna 15): perché qui non si può usare `json=`? Rispondete in una o due righe.

## ESERCIZIO 2: Fixture, stato pulito e servizi esterni (45 Punti)

**Parte A (20 punti).**

**2A.1 (13 punti)** Completate `conftest.py`.

```python
# conftest.py
import pytest
import requests


@pytest.fixture
def base_url():
    return "http://localhost:8000"


@pytest.fixture(__(17)__)              # deve girare prima di OGNI test, senza che nessun test la chieda
def stato_pulito(base_url):
    __(18)__                           # riporta il server allo stato iniziale


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json=__(19)__,
        timeout=5,
    )
    return __(20)__


@pytest.fixture
def auth(__(21)__):                    # auth USA un'altra fixture
    return __(22)__                    # l'header di autenticazione pronto all'uso
```

**2A.2 (7 punti)** Scrivete in `test_prestiti.py` un test che prende in prestito il libro `1` e poi verifica, **rileggendo il libro con una seconda chiamata**, che non sia più disponibile. Il test deve restare verde anche lanciando `pytest` dieci volte di fila.

**Parte B (25 punti).** Il client della Rete Bibliotecaria Regionale è `rete_regionale.py`:

```python
# rete_regionale.py — client della Rete Bibliotecaria Regionale (servizio esterno, NON è nostro)
import requests

RETE_URL = "https://rete.biblioteche.example/api"


class ReteNonDisponibile(Exception):
    """La rete regionale non risponde o risponde male: errore di DOMINIO, non di rete."""


def copie_in_rete(isbn: str) -> int:
    """Quante copie del libro si possono chiedere alle altre biblioteche della rete."""
    try:
        risposta = requests.get(f"{RETE_URL}/copie/{isbn}", timeout=2)
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise ReteNonDisponibile(str(errore)) from errore
    return risposta.json()["copie"]
```

I test vanno in `test_rete_regionale.py`, nella stessa cartella della Parte A (il server della biblioteca è acceso). **Nessun test deve contattare la rete regionale.**

**2B.1 (7 punti)** Completate il test del percorso felice: la rete risponde `{"copie": 3}`, la funzione restituisce `3` e la chiamata è stata fatta con un `timeout` di al massimo 2 secondi.

```python
# test_rete_regionale.py
from unittest.mock import MagicMock, patch

import pytest
import requests

from rete_regionale import ReteNonDisponibile, copie_in_rete


@patch(__(23)__)                       # regola del path: dove viene USATO
def test_copie_lette_dalla_risposta(mock_get):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = __(24)__
    mock_get.return_value = risposta_finta

    # Act
    copie = copie_in_rete("9788845292613")

    # Assert
    assert copie == 3
    _, kwargs = mock_get.call_args
    assert __(25)__                    # timeout di al massimo 2 secondi
```

**2B.2 (8 punti)** Scrivete un'**unica** funzione di test parametrizzata che simuli sia una rete che **non risponde in tempo** sia una rete **irraggiungibile**, e verifichi che in entrambi i casi venga sollevata `ReteNonDisponibile`.

**2B.3 (5 punti)** Scrivete un test in cui la rete **risponde**, ma con lo status `500`: anche in questo caso deve essere sollevata `ReteNonDisponibile`. La chiamata di rete riesce: è la **risposta** a contenere l'errore.

**2B.4 (5 punti)** I test con il mock sono verdi. Ora volete sapere se **la biblioteca intera** regge quando la rete regionale si guasta, con un esperimento come quello fatto in aula con il corriere della Bottega.

a) Scrivete l'**ipotesi** dell'esperimento, in una frase, con un numero che si possa misurare.

b) Cosa si aspetta l'utente da `POST /api/richieste-rete` (status code e tempo massimo di risposta) con la rete **spenta**? E con la rete **lenta** (10 secondi)?

c) Se in `rete_regionale.py` mancasse `timeout=2`, quale dei due scenari sarebbe il più pericoloso per gli utenti, e perché?
