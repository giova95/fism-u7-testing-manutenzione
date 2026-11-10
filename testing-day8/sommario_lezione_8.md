# RECAP GIORNO 8: il corriere, poi il primo sguardo al browser

La mattina abbiamo corretto insieme il compito: la Bottega dipende da un corriere esterno, e ora sa cosa fare quando il corriere non risponde. Poi abbiamo rotto il corriere per davvero, per vedere il sistema intero reagire. Alla fine abbiamo guardato la Bottega dal lato del cliente: un browser vero, comandato da Python. Il primo strumento che abbiamo provato, il registratore di Playwright, scrive codice da solo, ma quel codice non è ancora un test.
---

## 1. Il corriere: iniezione di guasti con il mock

Il mock di venerdì rispondeva sempre bene (`return_value`). Con `side_effect` invece **esplode**: è l'**iniezione di guasti**.

```python
@pytest.mark.parametrize("guasto", [
    requests.Timeout("il corriere non risponde"),
    requests.ConnectionError("il corriere è spento"),
])
@patch("spedizioni.requests.get")
def test_guasto_di_rete_diventa_errore_di_dominio(mock_get, guasto):
    mock_get.side_effect = guasto                      # il mock non risponde: esplode

    with pytest.raises(ServizioSpedizioniNonDisponibile):
        spedizioni.costo_spedizione("50100", 1.5)
```

- **Il timeout:** `mock_get.call_args` dice con quali parametri è stato chiamato il mock. Un test verifica che ci sia `timeout` e che sia al massimo 3 secondi.
- **Il 503 del corriere:** il corriere risponde, ma male. `risposta.raise_for_status()` solleva `requests.HTTPError` per gli status ≥ 400; nel mock si simula con `risposta_finta.raise_for_status.side_effect = requests.HTTPError("503")`.
- **Prima i test, rossi. Poi il codice.** Se importate un'eccezione che non esiste ancora, pytest si ferma con un errore di collection: si crea la classe vuota e i test diventano rossi "veri".

### Eccezioni di dominio

```python
class ServizioSpedizioniNonDisponibile(Exception):
    """Il corriere non ha risposto, o ha risposto male. Errore di DOMINIO, non di rete."""

def costo_spedizione(cap, peso):
    try:
        risposta = requests.get(f"{CORRIERE_URL}/tariffa", params={"cap": cap, "peso": peso}, timeout=3)
        risposta.raise_for_status()
    except requests.RequestException as errore:      # Timeout, ConnectionError, HTTPError...
        raise ServizioSpedizioniNonDisponibile(str(errore)) from errore
    return risposta.json()["costo"]
```

`app.py` non deve sapere che sotto c'è HTTP: cattura **solo** `ServizioSpedizioniNonDisponibile` e risponde `503` con `{"errore": "servizio spedizioni non disponibile"}`, **prima** di toccare stock e carrello. Se domani il corriere cambia tecnologia, cambia solo `spedizioni.py`.

---

## 2. Il corriere rotto per davvero: un assaggio di Chaos Engineering

Il mock dimostra che **la funzione** reagisce bene a un guasto **simulato**. Ma il sistema intero? L'abbiamo visto in aula rompendo l'ambiente per davvero (corriere spento con CTRL+C, poi riacceso con `CORRIERE_LATENZA=10`):

| Scenario | Codice ereditato | Codice corretto |
|----------|------------------|-----------------|
| Corriere spento | `500`, crash | `503` in pochi millisecondi, carrello salvo |
| Corriere lento (10s) | `201`... dopo **10 secondi** | `503` in 3 secondi, carrello salvo |

**⚠️ LA LEZIONE:** un fornitore **lento** è più pericoloso di un fornitore **spento**. Il guasto si nota subito; la lentezza no, e intanto ogni cliente occupa il server finché non lo satura. Il timeout non è un dettaglio: è l'unica difesa.

**Chaos Engineering** = rompere il sistema **apposta**, in modo **controllato**, per scoprire come si rompe **prima** che lo scopra il cliente.

```bash
pytest -m chaos      # i test marcati @pytest.mark.chaos si lanciano solo esplicitamente
```

---

## 3. In cima alla piramide

| Livello | Strumento | Velocità | Quanti test |
|---------|-----------|----------|-------------|
| Unit (white box) | pytest + `@patch` | millisecondi | tanti |
| API (black box) | `requests` | decine di millisecondi | un buon numero |
| **E2E / UI** | **Playwright** | **secondi** | **pochi, sui flussi critici** |

Più si sale, più il test è realistico, ma anche più lento, più fragile e meno preciso nel dire **dove** sta il guasto. I test E2E si scrivono solo per i flussi che, se si rompono, fanno perdere soldi: login, carrello, checkout.

---

## 4. Codegen: il registratore

```bash
python -m playwright codegen localhost:8000
```

Si aprono due finestre: un browser con la Bottega e l'Inspector, che mentre cliccate scrive il codice Python. Il risultato sembra un test, ma in code review non passa:

- **non c'è nemmeno un `expect`.** Se il checkout desse errore, sarebbe verde lo stesso. **Un test senza verifiche non è un test: è una registrazione;**
- l'URL è scritto a mano (`http://localhost:8000/`): su un altro computer o in CI l'indirizzo è un altro;
- il nome (`test_example`) non dice cosa verifica, e ci sono click inutili prima di ogni `fill`;
- `.first`: quale prodotto ha aggiunto? Lo sa solo chi l'ha registrato;
- per "Accedi" ha usato `get_by_role("button", ...)`, per "Aggiungi" un `locator("div")`. Sono due bottoni uguali a vedersi: perché? **Ci ripartiamo domani.**

Codegen è uno strumento **semi-automatico**: utile per scoprire come trovare un elemento nella pagina. Cosa verificare lo decidiamo noi.

---

## 5. Per domani

Domani si parte dal **lab sul browser** ([`lab1_primo_e2e/README.md`](lab1_primo_e2e/README.md)). Arrivate con Playwright già installato e funzionante, punto 2 di [`SETUP.md`](SETUP.md):

```bash
python -m playwright install chromium
```

Chi ha avuto problemi con il download lo segnali appena entra.

---

## 6. Documentazione Ufficiale (RTFM)

**Mock e chaos:**

- **unittest.mock (`patch`, `side_effect`, `call_args`):** https://docs.python.org/3/library/unittest.mock.html
- **requests, timeout:** https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
- **requests, eccezioni:** https://requests.readthedocs.io/en/latest/api/#exceptions
- **Marker di pytest (`-m chaos`):** https://docs.pytest.org/en/stable/how-to/mark.html
- **Principles of Chaos Engineering:** https://principlesofchaos.org/

**Playwright:**

- **Playwright per Python:** https://playwright.dev/python/docs/intro
- **Codegen:** https://playwright.dev/python/docs/codegen
