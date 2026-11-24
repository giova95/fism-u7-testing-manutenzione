let token = null;

// [G5] Versione minima della gestione errori: ogni chiamata passa da qui.
// Se il server non risponde, risponde con un errore o con HTML al posto di JSON (es. 502 del proxy),
// il cliente vede un messaggio chiaro invece di una pagina che "non fa niente".
async function chiamaApi(percorso, opzioni = {}) {
  let risposta;
  try {
    risposta = await fetch(percorso, opzioni);
  } catch (errore) {
    throw new Error("Il server non risponde. Riprova tra poco.");
  }
  let dati = null;
  try {
    dati = await risposta.json();
  } catch (errore) {
    // non era JSON
  }
  if (!risposta.ok) {
    throw new Error(dati && dati.errore ? `Errore: ${dati.errore}` : `Servizio non disponibile (${risposta.status}). Riprova tra poco.`);
  }
  return dati;
}

async function caricaCatalogo() {
  let prodotti;
  try {
    prodotti = await chiamaApi("/api/prodotti");
  } catch (errore) {
    mostraMessaggio(errore.message, true);
    return;
  }

  const catalogo = document.getElementById("catalogo");
  catalogo.innerHTML = "";
  for (const p of prodotti) {
    const scheda = document.createElement("div");
    scheda.className = "scheda";
    scheda.innerHTML = `
      <img src="${p.immagine}">
      <h3>${p.nome}</h3>
      <p class="prezzo">€ ${p.prezzo.toFixed(2)}</p>
      <div class="btn" onclick="aggiungi(${p.id})">Aggiungi</div>
    `;
    catalogo.appendChild(scheda);
  }
}

async function login(evento) {
  evento.preventDefault();
  const risposta = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
    }),
  });
  const dati = await risposta.json();
  if (!risposta.ok) {
    mostraMessaggio(dati.errore, true);
    return;
  }
  token = dati.token;
  document.getElementById("form-login").hidden = true;
  const benvenuto = document.getElementById("benvenuto");
  benvenuto.textContent = `Ciao ${document.getElementById("username").value}!`;
  benvenuto.hidden = false;
  document.getElementById("form-checkout").hidden = false;
  mostraMessaggio("");
  caricaCarrello();
}

async function caricaCarrello() {
  let dati;
  try {
    dati = await chiamaApi("/api/carrello", { headers: { Authorization: `Bearer ${token}` } });
  } catch (errore) {
    mostraMessaggio(errore.message, true);
    return;
  }
  const contenitore = document.getElementById("carrello");
  if (dati.righe.length === 0) {
    contenitore.innerHTML = '<p class="vuoto">Il carrello è vuoto</p>';
    return;
  }
  contenitore.innerHTML =
    "<ul>" +
    dati.righe.map((r) => `<li>${r.quantita} × ${r.nome} <span>€ ${r.subtotale.toFixed(2)}</span></li>`).join("") +
    "</ul>" +
    `<p class="totale">Totale: € ${dati.totale.toFixed(2)}</p>`;
}

async function aggiungi(prodottoId) {
  if (!token) {
    mostraMessaggio("Devi accedere prima di comprare", true);
    return;
  }
  try {
    await chiamaApi("/api/carrello", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ prodotto_id: prodottoId, quantita: 1 }),
    });
    mostraMessaggio("");
  } catch (errore) {
    mostraMessaggio(errore.message, true);
  }
  caricaCarrello();
}

let ordineInCorso = false;

async function confermaOrdine() {
  // [G5] Niente doppio click durante l'attesa: un secondo POST /api/ordini sarebbe un secondo ordine!
  if (ordineInCorso) return;
  ordineInCorso = true;
  mostraMessaggio("Ordine in corso...");
  try {
    const dati = await chiamaApi("/api/ordini", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        cap: document.getElementById("cap").value,
        codice_sconto: document.getElementById("codice-sconto").value,
      }),
    });
    mostraMessaggio(`Ordine n. ${dati.id} confermato! Totale pagato: € ${dati.totale.toFixed(2)}`);
    caricaCatalogo();
  } catch (errore) {
    mostraMessaggio(errore.message, true);
  } finally {
    ordineInCorso = false;
    caricaCarrello();
  }
}

function mostraMessaggio(testo, errore = false) {
  const box = document.getElementById("messaggio");
  box.textContent = testo;
  box.className = errore ? "errore" : "successo";
}

document.getElementById("form-login").addEventListener("submit", login);
caricaCatalogo();
