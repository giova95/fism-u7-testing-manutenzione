# Homework: il browser

## Contesto

Oggi abbiamo messo un browser robot davanti alla Bottega e abbiamo scoperto che alcuni bottoni non erano bottoni e alcuni campi non avevano un nome: chi non vede lo schermo, o non usa il mouse, non poteva comprare. Il compito chiude questo lavoro.

**Il Livello 1 è obbligatorio.** Se in aula siete arrivati alla correzione dell'HTML richiede circa un'ora; se vi siete fermati prima, contate un'ora in più. I tempi tra parentesi sono indicativi. Se vi bloccate, scrivete nel README del repository **dove** vi siete bloccati e **cosa** avete provato: conta anche quello.

> 🧩 **Prima di iniziare:** ripassate [`sommario_lezione_8.md`](../sommario_lezione_8.md). Se i test delle API vanno tutti in `ERROR` con `ScopeMismatch`, la cura è nello [`SETUP.md`](../SETUP.md), punto 2.

## Livello 1: Sopravvivenza (obbligatorio per tutti)

1. **Il test E2E del flusso d'acquisto** ([`lab1_primo_e2e/README.md`](../lab1_primo_e2e/README.md), **Livello 1**) (circa 40'):
   - `tests/e2e/test_acquisto.py` con `test_la_home_si_apre` e `test_acquisto_completo`, con i locator per ruolo ed etichetta della tabella del lab;
   - l'HTML corretto: `<label>` per Username, Password e CAP; `<button>` per "Aggiungi" e "Conferma ordine", con il checkout che parte dall'evento `submit` del form;
   - `pytest tests/e2e` verde, in headless, **due volte di fila**;
   - vietati `time.sleep()` e `wait_for_timeout()`.
2. **Il bug report** (circa 15'). Nel `BUG_REPORT.md` aggiungete una sezione **"Frontend"** con i difetti trovati dal test con i ruoli (campi senza etichetta, bottoni fatti con un `<div>`). Per ognuno scrivete **quale test** l'ha trovato e **chi** ne è colpito (chi usa un lettore di schermo? chi usa solo la tastiera?).
3. Un commit per ogni gruppo di correzioni, con il codice del bug nel messaggio (es. `fix: BUG-012 bottoni del catalogo non raggiungibili da tastiera`).

## Livello 2: Ingegneria (consigliato)

1. **Lo scanner** (lab, **Livello 2, punti 1-2**) (circa 40'): `tests/e2e/test_accessibilita.py` con axe, che asserisce **zero violazioni `critical` e `serious`** e quando fallisce dice **quali** regole e **quali** elementi. Correggete `lang`, `alt` e i design token del contrasto in `style.css`. Nel bug report aggiungete i difetti trovati da axe, con il criterio WCAG (1.1.1 *Contenuti non testuali*, 1.4.3 *Contrasto minimo*, 3.1.1 *Lingua della pagina*).
2. **Il Page Object Model** (lab, **Livello 2, punto 3**) (circa 40'): `tests/e2e/pagina_bottega.py`, la fixture `bottega` in `conftest.py` e `test_acquisto_completo` riscritto con il Page Object. `accedi()` torna solo quando compare il saluto. Nei file `test_*.py` non compare nessun `get_by_...`.

## Livello 3: Escalation (facoltativo, sceglietene quanti volete)

- **Sad path, tastiera e axe dopo il login** (lab, Livello 3).
- **Gli errori nell'interfaccia** ([`lab3_debugging_chaos_ui/README.md`](../lab3_debugging_chaos_ui/README.md)): `page.route` e il Trace Viewer, il catalogo che risponde `500`, la funzione `chiamaApi`.
- **La pipeline E2E:** un workflow GitHub Actions (`.github/workflows/e2e.yml`) che installa il browser con `python -m playwright install --with-deps chromium`, accende corriere e app in background, aspetta che rispondano (un ciclo con `curl`, non `sleep 10`) e lancia `pytest tests/e2e` in headless.

---

## Istruzioni per la consegna

1. Lavorate sullo **stesso repository privato**: il docente è già collaboratore. Controllate che `test-results/` **non** sia nel repo.
2. Mandate a `angeligiovanni21@gmail.com` il link al repository entro le **23:59 di domenica 22 novembre**.
