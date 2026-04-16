import pytest
from validatore import valida_password

def test_password_lunga():
    risultato = valida_password("123456789")
    assert risultato == True

def test_password_corta():
    with pytest.raises(ValueError, match="La password deve essere lunga almeno 8 caratteri."):
        valida_password("Ciao")

"""
def test_password_lunga():
    assert valida_password("PasswordLunga123") == True

def test_password_corta():
    with pytest.raises(ValueError, match="La password deve essere lunga almeno 8 caratteri."):
        valida_password("Ciao1")

def test_password_caratteri():
    with pytest.raises(ValueError, match="La password deve contenere almeno un numero."):
        valida_password("PasswordLunga")

def test_password_minuscola():
    with pytest.raises(ValueError, match="La password deve contenere almeno una maiuscola."):
        valida_password("passwordlunga12")
"""

@pytest.mark.parametrize("password, expected, match_msg", [
    ("PAsswordLunga456", True, None),
    ("", ValueError, "La password deve essere lunga almeno 8 caratteri.")
    ("pass456", ValueError, "La password deve essere lunga almeno 8 caratteri."),
    ("testCiao", ValueError, "La password deve contenere almeno un numero."),
    ("    Ciao123", True, None),
    ("             ", ValueError, "La password deve contenere almeno un numero."),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True),
    ("PAsswordLunga456", True)
])

def test_password_parametrize(password, expected, match_msg):
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected, match=match_msg):
            valida_password(password)
    else:
        assert (valida_password(password) == expected)