import pytest
from validatore import valida_password
from blacklist_db import carica_blacklist

# FIXTURE
@pytest.fixture(scope="session")
def blacklist_data():
    blacklist = carica_blacklist()
    
    yield blacklist


################ livello 1 e 2 ################################################
# Happy Path
def test_password_lunga():
    assert valida_password("PasswordLunga123") is True

def test_password_corta():
    with pytest.raises(ValueError, match="La password deve essere lunga almeno 8 caratteri."):
        valida_password("Ciao1")

def test_password_caratteri():
    with pytest.raises(ValueError, match="La password deve contenere almeno un numero."):
        valida_password("PasswordLunga")

def test_password_minuscola():
    with pytest.raises(ValueError, match="La password deve contenere almeno una maiuscola."):
        valida_password("passwordlunga12")

################ livello 3.1 parametrize ################################################

@pytest.mark.parametrize("password, expected, match_msg", [
    ("PAsswordLunga456", True, None),
    ("", ValueError, "La password deve essere lunga almeno 8 caratteri."),
    ("pass456", ValueError, "La password deve essere lunga almeno 8 caratteri."),
    ("testCiao", ValueError, "La password deve contenere almeno un numero."),
    ("    Ciao123", True, None),
    ("             ", ValueError, "La password deve contenere almeno un numero."),
    ("    cion12", ValueError, "La password deve contenere almeno una maiuscola."),
    ("    ", ValueError, "La password deve essere lunga almeno 8 caratteri."),
    ("PAsswordLunga/&", ValueError, "La password deve contenere almeno un numero."),
    ("passworda1???", ValueError, "La password deve contenere almeno una maiuscola."),
    ("passW32##@", True, None),
    ("123456789", ValueError, "La password deve contenere almeno una maiuscola."),
    ("ciaociao", ValueError, "La password deve contenere almeno un numero."),
    ("Password123", ValueError, "La password è compromessa."),
    ("Qwerty123", ValueError, "La password è compromessa."),
    ("\tPassword123\n", True, None)
])

def test_password_parametrize(password, expected, match_msg, blacklist_data):
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected, match=match_msg):
            valida_password(password, blacklist=blacklist_data)
    else:
        assert (valida_password(password) == expected)