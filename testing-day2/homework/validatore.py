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
        raise ValueError("PWD troppo corta")
    
    for c in password:
        if c.isupper():
            return True
        else:
            continue

    raise ValueError("PWD non ha maiuscole")

    for c in password:
        if c.isdigit():
            return True
        else:
            continue

    raise ValueError("PWD non ha numeri")
    
if __name__ == "__main__":
    pwd = "cane5"
    print(valida_password(pwd))