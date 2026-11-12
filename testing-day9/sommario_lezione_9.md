# RECAP GIORNO 9: il browser e la simulazione d'esame

La mattina abbiamo messo un browser robot davanti alla Bottega: il primo test scritto "come un utente" non trovava metà della pagina, e non era colpa del test. Abbiamo corretto l'HTML finché il test d'acquisto è diventato verde. Il pomeriggio: la simulazione d'esame al PC.

---

## 1. Il primo test con il browser

```python
from playwright.sync_api import Page, expect

def test_acquisto_completo(page: Page):
    # Arrange: apro la home e faccio login
    page.goto("/")
    page.get_by_label("Username").fill("mario")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Accedi").click()
    expect(page.get_by_text("Ciao mario!")).to_be_visible()

    # Act
    scheda = page.locator(".scheda").filter(has_text="Tastiera meccanica")
    scheda.get_by_role("button", name="Aggiungi").click()
    expect(page.get_by_text("1 × Tastiera meccanica")).to_be_visible()
    page.get_by_label("CAP").fill("50100")
    page.get_by_role("button", name="Conferma ordine").click()

    # Assert: quello che VEDE l'utente
    expect(page.get_by_text("Ordine n. 1 confermato! Totale pagato: € 89.90")).to_be_visible()
    expect(page.get_by_text("Il carrello è vuoto")).to_be_visible()
```

```bash
pytest tests/e2e --headed --slowmo 500    # lo guardo lavorare
pytest tests/e2e                          # senza finestra (headless): è così che gira in CI
```

**Le regole:**

- **I locator in quest'ordine:** `get_by_role` → `get_by_label` → `get_by_placeholder` / `get_by_text` → CSS (solo se non c'è alternativa, con un commento). Più si scende, più il test si rompe quando cambia la grafica.
- **Si verifica con `expect(...)`**, che riprova fino a 5 secondi. `assert locator.inner_text() == ...` legge una volta sola, subito.
- **⚠️ `time.sleep()` e `wait_for_timeout()` sono vietati.** Un'attesa fissa è lenta quando va bene e troppo corta quando la rete rallenta: il test diventa **flaky**.
- **Un test senza `expect` non è un test: è una registrazione** (il difetto di `codegen`).
- I test con il browser stanno in `tests/e2e/`, con il `conftest.py` del lab: accende i server se servono e chiama il reset prima di ogni test (la `stato_pulito`, che serve anche qui: il browser è nuovo a ogni test, il server no).

### Un test che usa i ruoli è anche un test di accessibilità

Playwright cerca gli elementi come li cerca un **lettore di schermo**: per **ruolo** e **nome**. Sulla Bottega originale il test si fermava subito: `waiting for get_by_label("Username")`. Quando un `expect` fallisce, sotto il `Call log` compare l'**Aria snapshot**, la pagina come la sentono le tecnologie assistive: "Accedi" era `button`, "Aggiungi" solo `text`.

| Difetto | Chi l'ha trovato | Correzione |
|---------|------------------|------------|
| campi con il solo placeholder | `get_by_label` | `<label for="id">` |
| bottoni fatti con `<div onclick>` | `get_by_role("button")` | un `<button>` vero |

**⚠️ Trappola:** un `<button>` dentro un `<form>` è `type="submit"`: senza `evento.preventDefault()` la pagina si ricarica e si perde il login. Ascoltando l'evento `submit` del form, l'ordine parte anche con Invio.

Se in aula non siete arrivati a `3 passed`, finite le correzioni a casa: è il **Livello 1 del compito della G3** (scadenza 22/11): le trappole sono descritte nel lab [`../testing-day8/lab1_primo_e2e/README.md`](../testing-day8/lab1_primo_e2e/README.md).

---

## 2. La simulazione d'esame

In aula avete fatto la teoria e l'Esercizio 1. **L'Esercizio 2 fatelo a casa, prima di guardare le soluzioni**: è la parte che vale di più all'esame (45 punti su 80 di pratica) e riprende fixture e mock, cioè i Lab 2 e 3. Il server della biblioteca si accende come in aula (`python server_biblioteca.py`).

Poi correggetevi con [`../esame-semestre2/soluzioni_simulazione/`](../esame-semestre2/soluzioni_simulazione/README.md): il `README.md` ha la chiave della teoria con il perché di ogni risposta, e le soluzioni degli esercizi spiegate lacuna per lacuna. Segnate i dubbi: li riprendiamo il 25/11 prima dell'esame. All'esame si lavora **su carta**, con il cheat sheet.

---

## 3. Documentazione Ufficiale (RTFM)

- **Playwright, locator:** https://playwright.dev/python/docs/locators
- **Playwright, auto-waiting:** https://playwright.dev/python/docs/actionability
- **Playwright, asserzioni `expect`:** https://playwright.dev/python/docs/test-assertions
- **Playwright, Aria snapshot:** https://playwright.dev/python/docs/aria-snapshots
- **WCAG 2.1 in breve:** https://www.w3.org/WAI/standards-guidelines/wcag/glance/
