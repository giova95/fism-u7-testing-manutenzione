import pytest

import preventivo


def pytest_addoption(parser):
    # pytest tests_preventivo --approva  ->  riscrive il golden master invece di confrontarlo
    parser.addoption(
        "--approva",
        action="store_true",
        help="riscrive tests_preventivo/approvato_preventivo.json con il comportamento ATTUALE",
    )


@pytest.fixture(autouse=True)
def sconti_puliti():
    """preventivo.SCONTI_USATI è una lista GLOBALE: senza pulizia i test dipendono dall'ordine."""
    preventivo.SCONTI_USATI.clear()
    yield
    preventivo.SCONTI_USATI.clear()
