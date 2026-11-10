"""
LAB 2 — Soluzione: autenticazione, fixture e stato distribuito.
"""

import pytest
import requests


def test_login_corretto_restituisce_token(base_url):
    risposta = requests.post(
        f"{base_url}/api/login",
        json={"username": "mario", "password": "password123"},
        timeout=5,
    )

    assert risposta.status_code == 200
    assert len(risposta.json()["token"]) > 0


@pytest.mark.parametrize(
    "headers",
    [
        {},  # nessun header
        {"Authorization": "Bearer token-inventato"},  # token falso
        {"Authorization": "token-senza-bearer"},  # formato sbagliato
    ],
)
def test_carrello_senza_autenticazione_401(base_url, headers):
    risposta = requests.get(f"{base_url}/api/carrello", headers=headers, timeout=5)

    assert risposta.status_code == 401


def test_aggiunta_al_carrello(base_url, auth):
    risposta = requests.post(
        f"{base_url}/api/carrello",
        json={"prodotto_id": 2, "quantita": 2},
        headers=auth,
        timeout=5,
    )

    assert risposta.status_code == 201
    assert risposta.json() == {"prodotto_id": 2, "quantita": 2}


# --- Livello 2: Ingegneria ---------------------------------------------------


def test_aggiunta_visibile_leggendo_il_carrello(base_url, auth):
    """Black box distribuito: non mi fido della risposta del POST, verifico lo stato con un'altra chiamata."""
    # Arrange
    requests.post(
        f"{base_url}/api/carrello",
        json={"prodotto_id": 2, "quantita": 2},
        headers=auth,
        timeout=5,
    )

    # Act
    carrello = requests.get(f"{base_url}/api/carrello", headers=auth, timeout=5).json()

    # Assert
    assert len(carrello["righe"]) == 1
    assert carrello["righe"][0]["quantita"] == 2
    assert carrello["totale"] == 69.00


@pytest.mark.parametrize(
    "body, status_atteso",
    [
        ({"prodotto_id": 2, "quantita": -3}, 400),  # quantità negativa
        ({"prodotto_id": 2, "quantita": 0}, 400),  # quantità zero
        ({"prodotto_id": 2, "quantita": "2"}, 400),  # tipo sbagliato
        ({"prodotto_id": 2}, 400),  # campo mancante
        ({"prodotto_id": 999, "quantita": 1}, 404),  # prodotto inesistente
        ({"prodotto_id": 3, "quantita": 99}, 409),  # oltre lo stock
    ],
)
def test_aggiunta_al_carrello_sad_paths(base_url, auth, body, status_atteso):
    risposta = requests.post(
        f"{base_url}/api/carrello", json=body, headers=auth, timeout=5
    )

    assert risposta.status_code == status_atteso
    assert "errore" in risposta.json()


@pytest.mark.parametrize(
    "username, password",
    [
        ("utente_che_non_esiste", "qualcosa"),
        ("mario", "password_sbagliata"),
    ],
)
def test_login_fallito_non_rivela_se_utente_esiste(base_url, username, password):
    risposta = requests.post(
        f"{base_url}/api/login",
        json={"username": username, "password": password},
        timeout=5,
    )

    assert risposta.status_code == 401
    assert risposta.json()["errore"] == "credenziali non valide"


# --- Livello 3: Escalation — il flusso completo (richiede corriere.py acceso) ----


def test_checkout_completo_scala_lo_stock(base_url, auth):
    # Arrange
    stock_prima = requests.get(f"{base_url}/api/prodotti/1", timeout=5).json()["stock"]
    requests.post(
        f"{base_url}/api/carrello",
        json={"prodotto_id": 1, "quantita": 2},
        headers=auth,
        timeout=5,
    )

    # Act
    ordine = requests.post(
        f"{base_url}/api/ordini", json={"cap": "50100"}, headers=auth, timeout=10
    )

    # Assert
    assert ordine.status_code == 201
    assert ordine.json()["totale"] == 179.80  # 2 x 89.90, spedizione gratis sopra 50€
    stock_dopo = requests.get(f"{base_url}/api/prodotti/1", timeout=5).json()["stock"]
    assert stock_dopo == stock_prima - 2
    carrello = requests.get(f"{base_url}/api/carrello", headers=auth, timeout=5).json()
    assert carrello["righe"] == []


def test_checkout_carrello_vuoto_400(base_url, auth):
    risposta = requests.post(
        f"{base_url}/api/ordini", json={"cap": "50100"}, headers=auth, timeout=10
    )

    assert risposta.status_code == 400
