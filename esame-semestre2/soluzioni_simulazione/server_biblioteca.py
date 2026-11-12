"""Server di verifica della SIMULAZIONE (biblioteca civica). Implementa il contratto stampato in simulazione_pratica.md.
La rete regionale non è simulata: /api/richieste-rete non serve a nessun test automatico (la 2B.4 è una domanda aperta)."""
import os
import copy, secrets
from flask import Flask, jsonify, request

app = Flask(__name__)
LIBRI = [
    {"id": 1, "titolo": "Il nome della rosa", "autore": "Umberto Eco", "disponibile": True},
    {"id": 2, "titolo": "La coscienza di Zeno", "autore": "Italo Svevo", "disponibile": True},
    {"id": 3, "titolo": "Il barone rampante", "autore": "Italo Calvino", "disponibile": False},
]
TESSERE = {"T-1001": "4321"}
stato = {}

def reset_stato():
    stato["libri"] = copy.deepcopy(LIBRI); stato["token"] = {}; stato["suggerimenti"] = []
reset_stato()

def errore(msg, status):
    return jsonify({"errore": msg}), status

@app.errorhandler(404)
def non_trovato(_):
    return errore("risorsa inesistente", 404)

@app.get("/api/libri")
def libri():
    q = request.args.get("q", "").lower()
    return jsonify([l for l in stato["libri"] if q in l["titolo"].lower()])

@app.get("/api/libri/<int:libro_id>")
def libro(libro_id):
    trovato = next((l for l in stato["libri"] if l["id"] == libro_id), None)
    return jsonify(trovato) if trovato else errore("libro inesistente", 404)

@app.post("/api/suggerimenti")
def suggerimenti():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or not isinstance(dati.get("titolo"), str) or not dati["titolo"].strip():
        return errore("body non valido", 400)
    stato["suggerimenti"].append(dati["titolo"])
    return jsonify({"titolo": dati["titolo"]}), 201

@app.post("/api/login")
def login():
    dati = request.get_json(silent=True) or {}
    if TESSERE.get(dati.get("tessera")) != dati.get("pin"):
        return errore("credenziali non valide", 401)
    token = secrets.token_hex(16); stato["token"][token] = dati["tessera"]
    return jsonify({"token": token})

@app.post("/api/prestiti")
def prestito():
    if request.headers.get("Authorization", "").removeprefix("Bearer ") not in stato["token"]:
        return errore("non autenticato", 401)
    dati = request.get_json(silent=True) or {}
    libro = next((l for l in stato["libri"] if l["id"] == dati.get("libro_id")), None)
    if libro is None:
        return errore("libro inesistente", 404)
    if not libro["disponibile"]:
        return errore("libro già in prestito", 409)
    libro["disponibile"] = False
    return jsonify({"libro_id": libro["id"]}), 201

@app.post("/api/reset")
def reset():
    reset_stato(); return jsonify({"stato": "ok"})

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "8000")))
