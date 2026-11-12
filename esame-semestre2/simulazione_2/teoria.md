# SIMULAZIONE 2 (guidata): Parte Teorica (30 minuti)

10 domande, una sola risposta corretta, 2 punti ciascuna. Le lettere vanno in `RISPOSTE.md`. Le domande dell'esame vero saranno **diverse**, ma sugli stessi argomenti.

1. Il contratto dice che `POST /api/recensioni` con un body valido crea una recensione. Quale status code vi aspettate?
   A) `200 OK`, perché la richiesta è andata a buon fine.
   B) `204 No Content`, perché il client conosce già il contenuto.
   C) `201 Created`: la richiesta ha **creato** una risorsa nuova, ed è lo status che il contratto chiede.
   D) `202 Accepted`, perché la recensione verrà salvata più tardi.

2. Un test chiama `POST /api/biglietti` **senza** l'header `Authorization`. Cosa vi aspettate da un'API scritta bene?
   A) `401 Unauthorized`: il server non sa chi siete, perché manca il token.
   B) `403 Forbidden`: il server sa chi siete, ma non avete il permesso.
   C) `400 Bad Request`: il body è sbagliato.
   D) `201 Created`: il biglietto è pubblico, il token serve solo per lo storico.

3. Un test chiede la fixture `auth`. Nel `conftest.py`, `auth` chiede `token`, e `token` chiede `base_url`. Cosa fa pytest?
   A) Si ferma con un errore: una fixture non può chiedere un'altra fixture.
   B) Esegue solo `auth`; `token` e `base_url` vanno chiamate a mano dentro il test.
   C) Esegue le tre fixture in ordine alfabetico.
   D) Costruisce la catena da solo: prima `base_url`, poi `token` (il login), poi `auth`, e consegna al test l'header pronto.

4. `pagamenti.py` fa `import requests` e chiama `requests.post(...)`. Quale `@patch` scrivete nei suoi test?
   A) `@patch("requests.post")`, perché `post` è definita nella libreria `requests`.
   B) `@patch("pagamenti.requests.post")`: si patcha **dove viene usato**, cioè nel modulo che fa la chiamata.
   C) `@patch("pagamenti.addebita")`, così il test non chiama niente.
   D) `@patch("test_pagamenti.requests.post")`, cioè nel file del test.

5. Volete che la chiamata finta a PagaSicuro **sollevi** `requests.ConnectionError`. Cosa scrivete?
   A) `mock_post.return_value = requests.ConnectionError()`
   B) `mock_post.status_code = 503`
   C) `mock_post.side_effect = requests.ConnectionError("irraggiungibile")`
   D) `raise requests.ConnectionError()` nell'Arrange del test.

6. Il contratto dice che ogni film ha **esattamente** i campi `id`, `titolo`, `durata`, `in_sala`. Nello schema avete messo i quattro campi in `properties` e in `required`. Cosa manca perché un film con un campo in più, per esempio `"regista"`, faccia fallire il test?
   A) `"additionalProperties": False`.
   B) Niente: `required` vieta già i campi in più.
   C) Un quinto campo in `required`.
   D) `"type": "array"` al posto di `"type": "object"`.

7. Il test del biglietto è verde se lo lanciate da solo, ma diventa rosso quando lo lanciate dopo un altro test che compra un biglietto per la stessa proiezione. Qual è la cura?
   A) Rinominare i test per farli girare sempre nello stesso ordine.
   B) Aggiungere `time.sleep(1)` all'inizio del test.
   C) Cambiare l'asserzione con `posti_liberi < 50`, così passa sempre.
   D) Una fixture `autouse` che chiama `POST /api/reset` prima di ogni test: ogni test parte dallo stesso stato noto.

8. Nella pagina c'è `<button>Acquista</button>`. Quale locator è il più robusto?
   A) `page.locator("body > div:nth-child(3) > button")`
   B) `page.get_by_role("button", name="Acquista")`
   C) `page.locator("button").nth(2)`
   D) `page.get_by_text("Acq")`

9. Dovete verificare 15 casi di body non validi per `POST /api/recensioni`. Dove li scrivete, secondo la piramide dei test?
   A) Come test dell'**API** con `requests`: sono veloci e stabili. Con il browser si verificano solo i pochi flussi importanti.
   B) Con Playwright, uno per caso: sono più realistici.
   C) Non si testano: il server li gestisce già.
   D) In un unico test E2E che li prova tutti di seguito, così si risparmia tempo.

10. Il test con il browser si ferma con `strict mode violation: get_by_role("button", name="Aggiungi") resolved to 4 elements`. Cosa fate?
    A) Aggiungete `time.sleep(2)`: la pagina non ha finito di caricare.
    B) Usate `page.locator(".btn").first`: tanto il primo va bene.
    C) Restringete la ricerca alla scheda giusta: `scheda = page.locator(".scheda").filter(has_text="Tastiera meccanica")` e poi `scheda.get_by_role("button", name="Aggiungi")`.
    D) Togliete tre bottoni dalla pagina.
