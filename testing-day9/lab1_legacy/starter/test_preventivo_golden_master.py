"""
La GABBIA: confronta il comportamento attuale con quello approvato.
Se un caso cambia, il test è rosso e dice QUALI casi sono cambiati.
"""

import pytest

import golden_master


def test_golden_master(request):
    # Act
    attuale = golden_master.fotografa()

    if request.config.getoption("--approva"):
        golden_master.salva(attuale)
        pytest.skip(f"golden master RISCRITTO ({len(attuale)} casi): controllate il diff prima del commit!")

    # Assert
    if not golden_master.FILE_APPROVATO.exists():
        pytest.fail("manca il file approvato: la PRIMA volta si lancia  pytest tests_preventivo --approva")
    approvato = golden_master.carica()
    assert len(attuale) == len(approvato), "sono cambiati i CASI, non solo i risultati: riapprovate consapevolmente"
    differenze = [
        f"{a} -> atteso {b['totale']}"
        for a, b in zip(attuale, approvato)
        if a != b
    ]
    assert not differenze, f"{len(differenze)} casi cambiati, i primi 10:\n" + "\n".join(differenze[:10])
