"""Server della SIMULAZIONE 3 (VeloCity, bike sharing). Implementa il contratto stampato in pratica.md.
È una scatola nera: si avvia e basta, non serve aprirlo. SbloccoBici non è simulato: nell'ambiente di test sblocca sempre."""
import copy
import os
import secrets

from flask import Flask, jsonify, request

app = Flask(__name__)
STAZIONI = [
    {"id": 1, "nome": "Stazione Centrale", "bici_libere": 5, "attiva": True},
    {"id": 2, "nome": "Piazza del Duomo", "bici_libere": 1, "attiva": True},
    {"id": 3, "nome": "Parco delle Cascine", "bici_libere": 0, "attiva": False},
]
UTENTI = {"luca.verdi": "Pedala2026"}
stato = {}


def reset_stato():
    stato["stazioni"] = copy.deepcopy(STAZIONI)
    stato["token"] = {}
    stato["segnalazioni"] = []
    stato["noleggi"] = []


reset_stato()


def errore(msg, status):
    return jsonify({"errore": msg}), status


def intero(valore):
    return isinstance(valore, int) and not isinstance(valore, bool)


def cerca_stazione(stazione_id):
    return next((s for s in stato["stazioni"] if s["id"] == stazione_id), None)


@app.errorhandler(404)
def non_trovato(_):
    return errore("risorsa inesistente", 404)


@app.errorhandler(405)
def metodo_non_ammesso(_):
    return errore("metodo non ammesso", 405)


@app.get("/api/stazioni")
def elenco_stazioni():
    return jsonify(stato["stazioni"])


@app.get("/api/stazioni/<int:stazione_id>")
def stazione(stazione_id):
    trovata = cerca_stazione(stazione_id)
    return jsonify(trovata) if trovata else errore("stazione inesistente", 404)


@app.post("/api/segnalazioni")
def segnalazioni():
    dati = request.get_json(silent=True)
    if (not isinstance(dati, dict) or not intero(dati.get("stazione_id"))
            or not isinstance(dati.get("testo"), str) or not dati["testo"].strip()):
        return errore("body non valido", 400)
    if cerca_stazione(dati["stazione_id"]) is None:
        return errore("stazione inesistente", 404)
    segnalazione = {"id": len(stato["segnalazioni"]) + 1, "stazione_id": dati["stazione_id"], "testo": dati["testo"]}
    stato["segnalazioni"].append(segnalazione)
    return jsonify(segnalazione), 201


@app.post("/api/login")
def login():
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or UTENTI.get(dati.get("utente")) != dati.get("password"):
        return errore("credenziali non valide", 401)
    token = secrets.token_hex(16)
    stato["token"][token] = dati["utente"]
    return jsonify({"token": token})


@app.post("/api/noleggi")
def noleggi():
    if request.headers.get("Authorization", "").removeprefix("Bearer ") not in stato["token"]:
        return errore("non autenticato", 401)
    dati = request.get_json(silent=True)
    if not isinstance(dati, dict) or not intero(dati.get("stazione_id")):
        return errore("body non valido", 400)
    stazione = cerca_stazione(dati["stazione_id"])
    if stazione is None:
        return errore("stazione inesistente", 404)
    if stazione["bici_libere"] == 0:
        return errore("nessuna bici libera", 409)
    stazione["bici_libere"] -= 1
    noleggio = {"id": len(stato["noleggi"]) + 1, "stazione_id": stazione["id"]}
    stato["noleggi"].append(noleggio)
    return jsonify(noleggio), 201


@app.post("/api/reset")
def reset():
    reset_stato()
    return jsonify({"stato": "ok"})


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "8000")))
