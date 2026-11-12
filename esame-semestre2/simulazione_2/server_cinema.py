"""Server della SIMULAZIONE 2 (Cinema Aurora). Implementa il contratto stampato in pratica.md.
È una scatola nera: si avvia e basta, non serve aprirlo. PagaSicuro non è simulato: nell'ambiente di test approva sempre."""
import copy
import os
import secrets

from flask import Flask, jsonify, request

app = Flask(__name__)
FILM = [
    {"id": 1, "titolo": "La grande bellezza", "durata": 141, "in_sala": True},
    {"id": 2, "titolo": "Nuovo Cinema Paradiso", "durata": 155, "in_sala": True},
    {"id": 3, "titolo": "Il sorpasso", "durata": 105, "in_sala": False},
]
PROIEZIONI = [
    {"id": 1, "film_id": 1, "posti_liberi": 50},
    {"id": 2, "film_id": 2, "posti_liberi": 1},
]
UTENTI = {"anna@aurora.it": "Popcorn24"}
stato = {}


def reset_stato():
    stato["proiezioni"] = copy.deepcopy(PROIEZIONI)
    stato["token"] = {}
    stato["recensioni"] = []
    stato["biglietti"] = []


reset_stato()


def errore(msg, status):
    return jsonify({"errore": msg}), status


def intero(valore):
    return isinstance(valore, int) and not isinstance(valore, bool)


@app.errorhandler(404)
def non_trovato(_):
    return errore("risorsa inesistente", 404)


@app.errorhandler(405)
def metodo_non_ammesso(_):
    return errore("metodo non ammesso", 405)


@app.get("/api/film")
def elenco_film():
    return jsonify(FILM)


@app.get("/api/film/<int:film_id>")
def film(film_id):
    trovato = next((f for f in FILM if f["id"] == film_id), None)
    return jsonify(trovato) if trovato else errore("film inesistente", 404)


@app.post("/api/recensioni")
def recensioni():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or not intero(dati.get("film_id")) or not intero(dati.get("voto")):
        return errore("body non valido", 400)
    if not any(f["id"] == dati["film_id"] for f in FILM):
        return errore("film inesistente", 404)
    stato["recensioni"].append(dati)
    return jsonify({"film_id": dati["film_id"], "voto": dati["voto"]}), 201


@app.post("/api/login")
def login():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or UTENTI.get(dati.get("email")) != dati.get("password"):
        return errore("credenziali non valide", 401)
    token = secrets.token_hex(16)
    stato["token"][token] = dati["email"]
    return jsonify({"token": token})


@app.get("/api/proiezioni/<int:proiezione_id>")
def proiezione(proiezione_id):
    trovata = next((p for p in stato["proiezioni"] if p["id"] == proiezione_id), None)
    return jsonify(trovata) if trovata else errore("proiezione inesistente", 404)


@app.post("/api/biglietti")
def biglietti():
    if request.headers.get("Authorization", "").removeprefix("Bearer ") not in stato["token"]:
        return errore("non autenticato", 401)
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or not intero(dati.get("proiezione_id")):
        return errore("body non valido", 400)
    proiezione = next((p for p in stato["proiezioni"] if p["id"] == dati["proiezione_id"]), None)
    if proiezione is None:
        return errore("proiezione inesistente", 404)
    if proiezione["posti_liberi"] == 0:
        return errore("posti esauriti", 409)
    proiezione["posti_liberi"] -= 1
    biglietto = {"id": len(stato["biglietti"]) + 1, "proiezione_id": proiezione["id"]}
    stato["biglietti"].append(biglietto)
    return jsonify(biglietto), 201


@app.post("/api/reset")
def reset():
    reset_stato()
    return jsonify({"stato": "ok"})


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "8000")))
