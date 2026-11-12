"""ESERCIZIO 2, Parte A, 2A.2 (7 punti).

Scrivete qui un test che noleggia l'unica bici della stazione 2 e poi verifica:
- RILEGGENDO la stazione con una seconda chiamata, che le bici libere siano 0;
- che un secondo noleggio alla stessa stazione risponda come dice il contratto.
Deve restare verde anche lanciando pytest dieci volte di fila.
"""

import requests

