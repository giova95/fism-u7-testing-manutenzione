"""
Smoke test: "il negozio è aperto e si può comprare?" — in meno di 10 secondi.

Non verificano TUTTO il contratto (per quello ci sono i test della G1): verificano il FLUSSO CRITICO
e un budget di tempo. Sono i primi da lanciare dopo una modifica e durante un incidente (G5).
Prerequisito: corriere.py e app.py accesi.
"""

import requests

BUDGET_SECONDI = 1.0   # oltre questo tempo, per il cliente il sito "è rotto" anche se risponde 200


def test_catalogo_veloce(base_url):
    risposta = requests.get(f"{base_url}/api/prodotti", timeout=5)
    assert risposta.status_code == 200
    assert risposta.elapsed.total_seconds() < BUDGET_SECONDI


def test_acquisto_completo(base_url, auth):
    aggiunta = requests.post(f"{base_url}/api/carrello", json={"prodotto_id": 4, "quantita": 1}, headers=auth, timeout=5)
    assert aggiunta.status_code == 201

    ordine = requests.post(f"{base_url}/api/ordini", json={"cap": "50100"}, headers=auth, timeout=10)
    assert ordine.status_code == 201, f"checkout fallito: {ordine.status_code} {ordine.text[:80]}"
    assert ordine.elapsed.total_seconds() < BUDGET_SECONDI, f"checkout lento: {ordine.elapsed.total_seconds():.1f}s"
