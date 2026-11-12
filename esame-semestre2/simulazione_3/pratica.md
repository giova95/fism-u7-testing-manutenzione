# SIMULAZIONE 3 (allenamento avanzato): Parte Pratica (90 minuti, 80 punti)

Stessa struttura dell'esame, ma **un po' più difficile**: meno lacune, e quattro test da scrivere **per intero** (all'esame ce n'è uno solo). Fatela dopo la simulazione 2, con il cronometro.

- **Al PC** (consigliato a casa): il codice è nelle cartelle `es1/` e `es2/` qui accanto, dove ogni lacuna `__(7)__` del testo è scritta `LACUNA(7)`. Istruzioni nel [`README.md`](README.md).
- **Su carta** (come all'esame): sul foglio scrivete il numero della lacuna e quello che va al suo posto, per esempio «(7) len(stazioni) > 0». Dove il testo dice «scrivete il test», scrivete la funzione intera.

Pattern Arrange-Act-Assert; ogni chiamata di rete ha un `timeout`.

## Il contesto: VeloCity, il bike sharing della città

Il backend di VeloCity espone un'API REST su `http://localhost:8000`. Il riferimento è **il contratto** qui sotto, non il codice del server: siete una scatola nera.

**Il contratto dell'API**

- Tutte le risposte sono JSON (`Content-Type: application/json`), errori compresi. Ogni errore ha la forma `{"errore": "..."}`. Il server non risponde **mai** `500` a causa dell'input del client.
- `GET /api/stazioni` → `200`, body: lista delle stazioni. Ogni stazione ha **esattamente** i campi `{"id": int, "nome": str, "bici_libere": int, "attiva": bool}`.
- `GET /api/stazioni/<id>` → `200` con la stazione. Stazione inesistente (anche se `<id>` non è un numero) → `404` con `{"errore": "..."}`.
- `POST /api/segnalazioni` (pubblico), body `{"stazione_id": int, "testo": str}` → `201`, body `{"id": int, "stazione_id": int, "testo": str}`. Stazione inesistente → `404`. Body non valido (JSON malformato, JSON che non è un oggetto, campo mancante, tipo sbagliato) → `400`.
- `POST /api/login`, body `{"utente": str, "password": str}` → `200`, body `{"token": str}`; credenziali errate → `401`. Utente di test: `luca.verdi` / `Pedala2026`.
- `POST /api/noleggi` (header `Authorization: Bearer <token>`), body `{"stazione_id": int}` → `201`, body `{"id": int, "stazione_id": int}`; nessuna bici libera nella stazione → `409`. Prima di confermare, VeloCity apre il lucchetto della bici con **SbloccoBici**, un servizio esterno: se SbloccoBici non risponde entro 2 secondi, o risponde con un errore → `503` con `{"errore": "servizio di sblocco non disponibile"}`. Nell'ambiente di test SbloccoBici sblocca sempre.
- `POST /api/reset` → `200`. Solo in ambiente di test: riporta i dati allo stato iniziale (stazione 1 con 5 bici libere, stazione 2 con 1 bici libera, stazione 3 non attiva e senza bici; nessun noleggio).

## ESERCIZIO 1: Black Box di un'API REST (35 Punti)

File `test_api_velocity.py`, con la libreria `requests`.

**1.1 (10 punti)** Completate lo scheletro: `GET /api/stazioni` (status, formato, lista non vuota) e **ogni** stazione rispetta lo schema del contratto.

```python
import pytest
import requests
from jsonschema import validate

BASE_URL = "http://localhost:8000"

SCHEMA_STAZIONE = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "nome": {"type": "string"},
        "bici_libere": __(1)__,
        "attiva": __(2)__,
    },
    "required": __(3)__,
    "additionalProperties": False,
}


def test_stazioni_rispettano_il_contratto():
    # Act
    risposta = requests.get(__(4)__, timeout=5)

    # Assert
    assert risposta.status_code == __(5)__
    assert risposta.headers["Content-Type"] == __(6)__
    stazioni = risposta.json()
    assert __(7)__                   # la lista non è vuota
    for stazione in stazioni:
        __(8)__                      # la stazione rispetta SCHEMA_STAZIONE
```

**1.2 (6 punti)** Completate lo scheletro: un **unico** test parametrizzato verifica che le stazioni `999`, `0` e `centrale` rispondano come dice il contratto per una stazione inesistente.

```python
@pytest.mark.parametrize("stazione_id", __(9)__)
def test_stazione_inesistente_risponde_404_in_json(stazione_id):
    # Act
    risposta = requests.get(f"{BASE_URL}/api/stazioni/{stazione_id}", timeout=5)

    # Assert
    __(10)__                         # lo status code
    __(11)__                         # la chiave "errore" nel body
```

**1.3 (6 punti)** Scrivete il test del percorso felice di `POST /api/segnalazioni`: stazione `1`, testo «freno rotto». Verificate lo status e il body restituito, campo per campo, come dice il contratto.

**1.4 (13 punti)** Completate lo scheletro: un **unico** test parametrizzato verifica che `POST /api/segnalazioni` risponda come dice il contratto a quattro body non validi. Ogni lacuna dei casi è una **stringa** Python.

```python
@pytest.mark.parametrize("body_grezzo", [
    '{"stazione_id": 1, "testo": "freno rotto"',     # JSON troncato (questo è già scritto)
    __(12)__,                        # manca il campo "testo"
    __(13)__,                        # stazione_id del tipo sbagliato
    __(14)__,                        # JSON valido, ma è una stringa e non un oggetto
])
def test_segnalazione_non_valida_risponde_400(body_grezzo):
    # Act
    risposta = requests.post(
        f"{BASE_URL}/api/segnalazioni",
        __(15)__,                    # la stringa va spedita così com'è
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    # Assert
    __(16)__                         # una o due righe: status e chiave "errore"
```

Domanda (lacuna 14): `"freno rotto"`, con le virgolette, è un JSON **valido**. Perché il server deve rifiutarlo? Rispondete in una o due righe.

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


@pytest.fixture(__(17)__)                      # deve girare prima di OGNI test, senza che nessun test la chieda
def stato_pulito(base_url):
    __(18)__                         # riporta il server allo stato iniziale


@pytest.fixture
def token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json=__(19)__,
        timeout=5,
    )
    return __(20)__


@pytest.fixture
def auth(__(21)__):                   # auth USA un'altra fixture: quale?
    return __(22)__                  # l'header di autenticazione pronto all'uso
```

**2A.2 (7 punti)** Scrivete in `test_noleggi.py` un test che noleggia l'unica bici della stazione `2` e poi verifica:
- **rileggendo la stazione con una seconda chiamata**, che le bici libere siano `0`;
- che un secondo noleggio alla stessa stazione risponda come dice il contratto.

Il test deve restare verde anche lanciando `pytest` dieci volte di fila.

**Parte B (25 punti).** Il client di SbloccoBici è `sblocco.py`:

```python
# sblocco.py — client di SbloccoBici (il servizio esterno che apre i lucchetti, NON è nostro)
import requests

SBLOCCO_URL = "https://api.sbloccobici.example"


class SbloccoNonDisponibile(Exception):
    """SbloccoBici non risponde o risponde male: errore di DOMINIO, non di rete."""


def sblocca(stazione_id: int, utente: str) -> bool:
    """Chiede a SbloccoBici di aprire il lucchetto di una bici della stazione. True se si è aperto."""
    try:
        risposta = requests.post(
            f"{SBLOCCO_URL}/sblocchi",
            json={"stazione_id": stazione_id, "utente": utente},
            timeout=2,
        )
        risposta.raise_for_status()
    except requests.RequestException as errore:
        raise SbloccoNonDisponibile(str(errore)) from errore
    return risposta.json()["sbloccata"]
```

I test vanno in `test_sblocco.py`. **Nessun test deve contattare SbloccoBici.**

```python
# test_sblocco.py
from unittest.mock import MagicMock, patch

import pytest
import requests

from sblocco import SbloccoNonDisponibile, sblocca
```

**2B.1 (7 punti)** Completate il test del percorso felice: SbloccoBici risponde `{"sbloccata": True}`, la funzione restituisce `True`, la chiamata è stata fatta con un `timeout` di al massimo 2 secondi e il body inviato contiene la stazione giusta.

```python
@patch(__(23)__)             # Regola del path: dove viene USATO
def test_lucchetto_aperto(mock_post):
    # Arrange
    risposta_finta = MagicMock()
    risposta_finta.status_code = 200
    risposta_finta.json.return_value = __(24)__
    mock_post.return_value = risposta_finta

    # Act
    sbloccata = sblocca(2, "luca.verdi")

    # Assert
    assert sbloccata is True
    _, kwargs = mock_post.call_args
    assert __(25)__                  # timeout di al massimo 2 secondi
    assert __(26)__                  # nel body inviato, la stazione è la 2
```

**2B.2 (8 punti)** Scrivete un'**unica** funzione di test parametrizzata che simuli sia SbloccoBici che **non risponde in tempo** sia SbloccoBici **irraggiungibile**, e verifichi che in entrambi i casi venga sollevata `SbloccoNonDisponibile`.

**2B.3 (5 punti)** Scrivete un test in cui SbloccoBici **risponde**, ma con lo status `500`: anche in questo caso deve essere sollevata `SbloccoNonDisponibile`.

**2B.4 (5 punti)** I test con il mock sono verdi. Ora volete sapere se **VeloCity intera** regge quando SbloccoBici si guasta, con un esperimento come quello fatto in aula con il corriere della Bottega.

a) Scrivete l'**ipotesi** dell'esperimento, in una frase, con un numero che si possa misurare.

b) Con SbloccoBici **spento**, cosa si aspetta l'utente da `POST /api/noleggi` (status code e tempo massimo di risposta)? E con SbloccoBici **lento** (10 secondi)?

c) Perché questo esperimento **non** si può sostituire con i test con il mock della Parte B? Cosa verifica l'uno e cosa verifica l'altro?
