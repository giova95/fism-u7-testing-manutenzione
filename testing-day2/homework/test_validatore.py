import pytest 
from validatore import valida_password

def test_password_lunga():
    risultato = valida_password("asdfghjkl1")
    assert risultato == True

def test_password_corta():
    with pytest.raises(ValueError, match="La password deve contenere almeno 8 caratteri"):
        valida_password("123456")

def test_numero():
    with pytest.raises(ValueError, match="La Password deve contenere almeno un numero"):
        valida_password("asdfdf2")
