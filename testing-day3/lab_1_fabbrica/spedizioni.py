def calcola_spedizione(peso: float, zona: str) -> float:
    if peso <= 0:
        raise ValueError("Il peso deve essere positivo")
    if zona == "EU":
        return 5.0 if peso < 2.0 else 10.0
    elif zona == "USA":
        return 15.0 if peso < 2.0 else 25.0
    else:
        raise ValueError("Zona non supportata")