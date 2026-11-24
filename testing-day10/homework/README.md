# Homework: l'ultimo rapporto (e, se volete, la Bottega che regge)

## Contesto

Oggi avete rotto la Bottega di proposito e avete visto che "funziona" e "regge" sono due cose diverse. È l'ultimo compito del modulo, ed è corto: il Livello 1 è il minimo per la sufficienza e richiede circa **un'ora**. Il Livello 2 e il Livello 3 sono facoltativi.

Consegnate nel **vostro** repository della Bottega (quello che portate avanti dalla G1), in una cartella `g5/`.

## Livello 1: Sopravvivenza (obbligatorio per tutti)

1. **L'esperimento.** Copiate in `g5/ESPERIMENTI.md` il file del Lab 1, con l'ipotesi, i numeri **reali** di `misura.py` (sistema sano e corriere al 30%) e la traccia compilata. Se in aula non l'avete finito, rifate il Lab 1 a casa: dura un quarto d'ora.
2. **Il postmortem.** Copiate `lab2_game_day/POSTMORTEM_TEMPLATE.md` in `g5/POSTMORTEM_GAMEDAY.md` e compilatelo per l'incidente che la vostra squadra ha **subìto** nel Game Day. Ognuno consegna la propria versione. Vincoli:
   - il Sommario è di 3 righe, senza gergo;
   - la timeline ha gli orari e le fonti (misura.py, pytest, browser, curl, log): la prendete da `INCIDENTE.md`, il file che lo Scriba ha mandato alla squadra;
   - **2** azioni correttive, ognuna con un owner;
   - **blameless**: nessun nome come causa.

## Livello 2: Ingegneria (facoltativo) — la difesa con il retry

Nel Lab 1 il 30% di errori del corriere diventava il 30% di checkout falliti. Una difesa è il **retry**: se una chiamata fallisce per un problema **passeggero**, riprovare dopo un attimo spesso funziona. Ma il retry è un'arma carica. Le **quattro regole**:

| Regola | Perché |
|--------|--------|
| 1. Solo su operazioni **idempotenti** | `GET /tariffa` chiesto 3 volte dà lo stesso risultato. `POST /api/ordini` chiesto 3 volte crea **3 ordini** |
| 2. Solo su errori **transitori** | 503 / connessione rifiutata: forse passa. 400: è sbagliato l'input, fallirà sempre uguale |
| 3. **Backoff esponenziale** con un po' di casualità (*jitter*) | aspettare 0,1s, poi 0,2s, poi 0,4s... dà respiro al fornitore. Il jitter evita che mille client riprovino tutti nello stesso istante |
| 4. Un **limite** | massimo 3 tentativi. Un retry infinito è un attacco al vostro stesso fornitore |

Fatelo in `bottega_g5` (la copia dell'aula):

1. Prima la misura senza difese, con il corriere instabile: terminale 1 `python chaos_ctl.py corriere --errori 0.3`, terminale 3 `python misura.py --checkout 100`.
2. Aprite `spedizioni.py`, **cancellate tutto** e incollate questo (la libreria `tenacity` è già in `requirements.txt`):

```python
"""
Client del servizio esterno del corriere (SpediVeloce S.p.A.).
Il servizio NON è nostro: non possiamo modificarlo, possiamo solo chiamarlo.

G5: aggiunto il retry, con le quattro regole.
"""

import logging
import os

import requests
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

CORRIERE_URL = os.getenv("CORRIERE_URL", "http://localhost:8001")
TIMEOUT_SECONDI = 3
STATUS_TRANSITORI = {502, 503, 504}   # "riprova più tardi": probabilmente passa da solo

log = logging.getLogger(__name__)


class ServizioSpedizioniNonDisponibile(Exception):
    """Il corriere non ha risposto, o ha risposto male. Errore di DOMINIO, non di rete."""


class ErroreTransitorio(Exception):
    """Un guasto del corriere per cui ha senso RIPROVARE."""


# REGOLA 1: GET /tariffa è idempotente (chiederla 3 volte non cambia niente): riprovare è sicuro.
# Il timeout (requests.ReadTimeout) NON diventa ErroreTransitorio: non si riprova (3 tentativi da 3 secondi = 9 secondi di attesa).
@retry(
    retry=retry_if_exception_type(ErroreTransitorio),                     # REGOLA 2: solo errori transitori
    stop=stop_after_attempt(3),                                           # REGOLA 4: un limite
    wait=wait_exponential_jitter(multiplier=0.1, max=1.0, jitter=0.1),    # REGOLA 3: backoff + jitter
    before_sleep=before_sleep_log(log, logging.WARNING),                  # ogni retry lascia una riga nel log
    reraise=True,
)
def _chiedi_tariffa(cap: str, peso: float) -> float:
    try:
        risposta = requests.get(
            f"{CORRIERE_URL}/tariffa",
            params={"cap": cap, "peso": peso},
            timeout=TIMEOUT_SECONDI,
        )
    except requests.ConnectionError as errore:        # corriere spento: forse torna
        raise ErroreTransitorio(f"connessione fallita: {errore}") from errore
    if risposta.status_code in STATUS_TRANSITORI:     # 502/503/504: forse passa
        raise ErroreTransitorio(f"il corriere ha risposto {risposta.status_code}")
    risposta.raise_for_status()                       # 4xx: input sbagliato, inutile riprovare
    return risposta.json()["costo"]


def costo_spedizione(cap: str, peso: float) -> float:
    """Quella che chiama app.py: stessa firma e stessa eccezione di prima."""
    try:
        return _chiedi_tariffa(cap, peso)
    except (ErroreTransitorio, requests.RequestException) as errore:
        # Traduco un problema tecnico in un problema di business (come nel Lab 3 sul corriere)
        raise ServizioSpedizioniNonDisponibile(str(errore)) from errore
```

**Perché due funzioni:** il `@retry` sta sulla funzione **interna** `_chiedi_tariffa`, che solleva `ErroreTransitorio` solo quando ha senso riprovare. `costo_spedizione` resta quella che chiama `app.py`, con la stessa eccezione di prima: per il resto del codice non cambia niente.

> **La riga con la `@`** è un *decoratore*: avvolge la funzione e le aggiunge un comportamento. L'avete già usato con `@pytest.fixture` e `@patch`. Qui, quando `app.py` chiama `_chiedi_tariffa`, in realtà chiama `tenacity`, che la richiama fino a 3 volte.

3. Salvate: `app.py` si riavvia da solo (nel terminale 2 compare `Restarting`). Rimisurate con `python misura.py --checkout 100`. Nel terminale 2 ogni riga `Retrying ...` è una chiamata **in più** al corriere.
4. Aggiungete a `g5/ESPERIMENTI.md`:
   - gli errori del checkout **senza** e **con** il retry;
   - il conto: tre tentativi falliscono tutti con probabilità 0,3 × 0,3 × 0,3 = ???%. Il numero misurato è vicino?
   - perché il retry si mette sulla richiesta della **tariffa** (GET) e **mai** sulla creazione dell'ordine (POST)? (regola 1)

## Livello 3: Escalation (facoltativo) — i test della difesa, con i mock

Create `tests/test_resilienza.py` in `bottega_g5`. Nessun server acceso: il corriere è un `MagicMock`, come nel Lab 3 sul corriere.

1. Il corriere risponde 503 e poi 200 → `costo_spedizione` restituisce il costo e `mock_get.call_count == 2`.
2. Il corriere risponde sempre 503 → `ServizioSpedizioniNonDisponibile` dopo **esattamente 3** chiamate.

> 🧩 **Non sai da dove partire?** Scheletro dei primi due test:
>
> ```python
> from unittest.mock import MagicMock, patch
>
> import pytest
> import requests
>
> import spedizioni
>
>
> @pytest.fixture(autouse=True)
> def stato_pulito():
>     """Sostituisce la fixture del conftest (che chiama il server): qui il server non serve."""
>     yield
>
>
> def risposta_finta(status, costo=4.90):
>     finta = MagicMock()
>     finta.status_code = status
>     finta.json.return_value = {"costo": costo}
>     if status >= 400:
>         finta.raise_for_status.side_effect = requests.HTTPError(str(status))
>     return finta
>
>
> @patch("spedizioni.requests.get")
> def test_un_503_passeggero_viene_assorbito(mock_get):
>     mock_get.side_effect = [risposta_finta(???), risposta_finta(???)]   # una risposta diversa a ogni chiamata
>
>     costo = spedizioni.costo_spedizione("50100", 1.0)
>
>     assert costo == ???
>     assert mock_get.call_count == ???
>
>
> @patch("spedizioni.requests.get")
> def test_sempre_503_dopo_tre_tentativi_eccezione_di_dominio(mock_get):
>     mock_get.return_value = risposta_finta(???)                        # sempre la stessa risposta
>
>     with pytest.raises(spedizioni.???):
>         spedizioni.costo_spedizione("50100", 1.0)
>
>     assert mock_get.call_count == ???
> ```
>
> Si lanciano con `pytest tests/test_resilienza.py`, anche a server spenti.

---

## Istruzioni per la consegna

1. Lavorate nel repository **privato** su GitHub della vostra Bottega (già condiviso con il docente). Controllate che `venv/` **non** sia nel repo. Per i Livelli 2 e 3 aggiungete in `g5/` anche il vostro `spedizioni.py` e `test_resilienza.py`.
2. Mandate il link del repository a `angeligiovanni21@gmail.com` entro le 23:59 di **lunedì 30/11**.

## Documentazione

- Google SRE Book, *Postmortem Culture: Learning from Failure*: https://sre.google/sre-book/postmortem-culture/
- tenacity (retry, stop, wait): https://tenacity.readthedocs.io/en/latest/
- Metodi HTTP idempotenti (MDN): https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
- unittest.mock, `side_effect` con una lista: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
