# validatore.py

def valida_password(password: str) -> bool:
    """
    Verifica che la password rispetti i requisiti aziendali.
    - Minimo 8 caratteri
    - Almeno una maiuscola
    - Almeno un numero
    
    Nel Livello 2: Modificare per lanciare ValueError con messaggi specifici.
    """
    if len(password) < 8:
        raise ValueError("La password deve contenere almeno 8 caratteri")


    elif not any(n.isnumeric() for n in password):
        raise ValueError("La Password deve contenere almeno un numero")
    


    return True