"""
chaos.py — iniezione di guasti CONTROLLATA nella Bottega (G5, Chaos Engineering Game Day).

Che cosa fa: prima di ogni richiesta HTTP (before_request) controlla se c'è una "regola di caos"
che riguarda quell'endpoint e, se sì, la applica:

    latenza   la risposta arriva N secondi più tardi             (il server è lento)
    errori    una percentuale di risposte diventa 500 o 503      (il server è instabile)
    kill      l'endpoint risponde 502 con una pagina HTML,        (il processo dietro al proxy è morto,
              come farebbe il proxy davanti a un'app morta         ad es. il proxy di un hosting)

In più può spostare l'OROLOGIO letto da preventivo.py (data_finta): il "caos del tempo".

Come si comanda: con l'endpoint di amministrazione /api/chaos (di solito tramite chaos_ctl.py).
    GET    /api/chaos   -> configurazione attuale
    PUT    /api/chaos   -> sostituisce la configurazione  {"regole": [...], "data_finta": "AAAA-MM-GG" | null}
    DELETE /api/chaos   -> KILL SWITCH: spegne subito ogni guasto

Le tre regole di sicurezza di questo modulo:
    1. In produzione (BOTTEGA_ENV=produzione) non viene nemmeno registrato: l'endpoint non esiste (404).
    2. /api/chaos risponde solo a richieste che arrivano dalla macchina stessa (localhost).
    3. /api/chaos non è mai soggetto al caos: il pulsante di emergenza deve funzionare SEMPRE.
"""

import datetime
import random
import time
from dataclasses import asdict, dataclass

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, Forbidden

import preventivo

PERCORSO_ADMIN = "/api/chaos"
INDIRIZZI_LOCALI = {"127.0.0.1", "::1"}
METODI_HTTP = {"GET", "POST", "PUT", "DELETE"}


@dataclass(frozen=True)
class Regola:
    """Un guasto da iniettare sulle richieste il cui percorso inizia con `percorso`."""

    percorso: str                 # es. "/api/prodotti" colpisce anche "/api/prodotti/3"
    metodo: str | None = None     # None = tutti i metodi
    latenza: float = 0.0          # secondi di ritardo aggiunti
    errori: float = 0.0           # probabilità di errore, da 0.0 a 1.0
    status: int = 503             # quale errore restituire: 500 o 503
    kill: bool = False            # True = l'endpoint è "morto"

    def __post_init__(self):
        # Validazione: una regola sbagliata non deve mai far esplodere il server (lezione della G1).
        if not isinstance(self.percorso, str) or not self.percorso.startswith("/"):
            raise ValueError("percorso deve iniziare con /")
        if self.percorso.startswith(PERCORSO_ADMIN):
            raise ValueError("il kill switch /api/chaos non si può rompere")
        if self.metodo is not None and self.metodo not in METODI_HTTP:
            raise ValueError(f"metodo deve essere uno tra {sorted(METODI_HTTP)}")
        if not 0 <= self.latenza <= 30:
            raise ValueError("latenza deve essere tra 0 e 30 secondi")
        if not 0 <= self.errori <= 1:
            raise ValueError("errori deve essere una probabilità tra 0 e 1")
        if self.status not in (500, 503):
            raise ValueError("status deve essere 500 o 503")

    def colpisce(self, percorso: str, metodo: str) -> bool:
        return percorso.startswith(self.percorso) and self.metodo in (None, metodo)


# Lo stato del caos. Viene SOSTITUITO in blocco (mai modificato a pezzi): così una richiesta
# in corso vede sempre una configurazione coerente, anche con il server multi-thread.
_regole: tuple[Regola, ...] = ()
_data_finta: datetime.date | None = None


# --- Il middleware ------------------------------------------------------------------

def _inietta_guasto():
    """Eseguita da Flask PRIMA di ogni richiesta. Se restituisce una risposta, l'endpoint non viene chiamato."""
    if request.path.startswith(PERCORSO_ADMIN):
        return None

    for regola in _regole:
        if not regola.colpisce(request.path, request.method):
            continue
        if regola.latenza:
            time.sleep(regola.latenza)
        if regola.kill:
            # Né JSON né contratto: è il proxy che parla, non la Bottega.
            return "<html><body><h1>502 Bad Gateway</h1></body></html>", 502, {"Content-Type": "text/html"}
        if random.random() < regola.errori:
            # Stesso formato degli errori veri (vedi errorhandler in app.py): da fuori è indistinguibile.
            messaggio = "internal server error" if regola.status == 500 else "service unavailable"
            return jsonify({"errore": messaggio}), regola.status
    return None


# --- Il caos del tempo --------------------------------------------------------------

def _imposta_orologio(data: datetime.date | None) -> None:
    """Fa credere a preventivo.py che oggi sia `data` (None = torna all'orologio vero).

    È la stessa tecnica di librerie come freezegun: si sostituisce il modulo `datetime`
    VISTO DA preventivo.py. Funziona solo perché preventivo legge `datetime.date.today()`
    direttamente: la cura vera è passare la data come parametro.
    """
    if data is None:
        preventivo.datetime = datetime
        return

    class DataFinta(datetime.date):
        @classmethod
        def today(cls):
            return data

    class ModuloDatetimeFinto:
        date = DataFinta

    preventivo.datetime = ModuloDatetimeFinto


# --- L'endpoint di amministrazione --------------------------------------------------

def _solo_da_localhost():
    if request.remote_addr not in INDIRIZZI_LOCALI:
        raise Forbidden("il pannello del caos si usa solo dalla macchina locale")


def _configurazione_attuale():
    return {
        "regole": [asdict(r) for r in _regole],
        "data_finta": _data_finta.isoformat() if _data_finta else None,
    }


def _leggi_configurazione(dati) -> tuple[tuple[Regola, ...], datetime.date | None]:
    if not isinstance(dati, dict):
        raise BadRequest("il body deve essere un oggetto JSON")
    try:
        regole = tuple(Regola(**r) for r in dati.get("regole", []))
        data = dati.get("data_finta")
        data_finta = datetime.date.fromisoformat(data) if data else None
    except (TypeError, ValueError) as errore:
        raise BadRequest(f"configurazione non valida: {errore}")
    return regole, data_finta


def leggi_stato():
    _solo_da_localhost()
    return jsonify(_configurazione_attuale())


def cambia_stato():
    global _regole, _data_finta
    _solo_da_localhost()
    nuove_regole, nuova_data = _leggi_configurazione(request.get_json(silent=True))
    _regole, _data_finta = nuove_regole, nuova_data
    _imposta_orologio(nuova_data)
    return jsonify(_configurazione_attuale())


def spegni_tutto():
    """KILL SWITCH: ogni esperimento serio ha un pulsante rosso per fermarlo subito."""
    global _regole, _data_finta
    _solo_da_localhost()
    _regole, _data_finta = (), None
    _imposta_orologio(None)
    return jsonify(_configurazione_attuale())


def registra(app: Flask, ambiente: str) -> None:
    """Collega il chaos middleware all'app. In produzione non fa NIENTE."""
    if ambiente == "produzione":
        return
    app.before_request(_inietta_guasto)
    app.add_url_rule(PERCORSO_ADMIN, "chaos_leggi", leggi_stato, methods=["GET"])
    app.add_url_rule(PERCORSO_ADMIN, "chaos_cambia", cambia_stato, methods=["PUT"])
    app.add_url_rule(PERCORSO_ADMIN, "chaos_spegni", spegni_tutto, methods=["DELETE"])
