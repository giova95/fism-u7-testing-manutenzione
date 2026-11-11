"""Segnaposto delle lacune. NON modificate questo file.

LACUNA(7) vuol dire: «qui va quello che chiede la lacuna (7) del testo».
Finché c'è, il test che la usa fallisce con il messaggio «la lacuna (7) non è ancora completata».
"""

import sys


class _Lacuna:
    def __init__(self, numero):
        self.numero = numero

    def __iter__(self):                # così una lacuna dentro @parametrize non blocca tutto il file
        return iter([self])

    def __repr__(self):
        return f"LACUNA({self.numero})"


def LACUNA(numero):
    if sys._getframe(1).f_code.co_name == "<module>":
        return _Lacuna(numero)         # fuori dai test: fallirà il test che la usa
    raise NotImplementedError(f"la lacuna ({numero}) non è ancora completata")
