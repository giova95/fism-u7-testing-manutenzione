"""
Difetti NOTI della Bottega: documentati come test, non dimenticati in una mail.

- xfail(strict=True): "so che questo test fallisce, ed è un bug registrato".
  Se un giorno il bug viene corretto, il test passa -> XPASS -> con strict=True la suite
  diventa ROSSA e vi obbliga a togliere l'xfail. Il registro dei difetti resta sempre vero.
- skip: "questo controllo oggi non si può eseguire", con il motivo scritto.

Nel report (pytest-html, JUnit, riepilogo CI) compaiono in colonne separate:
è esattamente la sezione "difetti noti" del Test Report per il CTO.
Prerequisito: app.py e corriere.py accesi (sono test black box).
"""

import pytest
import requests


def ordina(base_url, auth, prodotto_id, quantita, cap, codice_sconto=""):
    """Arrange + Act di un ordine completo: carrello -> checkout. Restituisce la risposta del checkout."""
    aggiunta = requests.post(
        f"{base_url}/api/carrello",
        json={"prodotto_id": prodotto_id, "quantita": quantita},
        headers=auth,
        timeout=5,
    )
    assert aggiunta.status_code == 201, "Precondizione fallita: non riesco a riempire il carrello"
    return requests.post(
        f"{base_url}/api/ordini",
        json={"cap": cap, "codice_sconto": codice_sconto},
        headers=auth,
        timeout=10,
    )


def nuovo_login(base_url):
    risposta = requests.post(
        f"{base_url}/api/login", json={"username": "mario", "password": "password123"}, timeout=5
    )
    return {"Authorization": f"Bearer {risposta.json()['token']}"}


@pytest.mark.xfail(
    strict=True,
    reason="DEC-001 (da decidere col business): sopra 49,99 euro la maggiorazione isole di 5 euro sparisce",
)
def test_maggiorazione_isole_anche_con_spedizione_gratuita(base_url, auth):
    # Monitor 249 euro, CAP 09100 (Cagliari). Ipotesi del commerciale 2022: "+5 euro per le isole, sempre".
    risposta = ordina(base_url, auth, prodotto_id=3, quantita=1, cap="09100")

    assert risposta.status_code == 201
    assert risposta.json()["totale"] == pytest.approx(254.00)


@pytest.mark.xfail(
    strict=True,
    reason="BUG-009 (= ticket BOT-42): BENVENUTO10 è salvato in una lista GLOBALE, vale una volta per tutto il server e /api/reset non lo azzera",
)
def test_benvenuto10_valido_dopo_reset(base_url, auth):
    # Arrange: qualcuno ha già usato il codice (oggi, ieri, in un altro test...)
    ordina(base_url, auth, prodotto_id=2, quantita=1, cap="50100", codice_sconto="BENVENUTO10")
    requests.post(f"{base_url}/api/reset", timeout=5)   # contratto: "riporta i dati allo stato iniziale"
    auth_dopo_reset = nuovo_login(base_url)              # il reset ha invalidato i token

    # Act: mouse 34,50 - 10 di sconto + 4,90 di spedizione
    risposta = ordina(base_url, auth_dopo_reset, prodotto_id=2, quantita=1, cap="50100", codice_sconto="BENVENUTO10")

    # Assert
    assert risposta.status_code == 201
    assert risposta.json()["totale"] == pytest.approx(29.40)


@pytest.mark.skip(reason="BUG-010: BLACKFRIDAY dipende da date.today(), non testabile senza controllare l'orologio")
def test_blackfriday_applica_sconto_20_percento(base_url, auth):
    ...
