import pytest
from validatore import valida_password

def test_password_corta():
    with pytest.raises(ValueError, match="PWD troppo corta"):
        valida_password("ciao")

def test_password_maiuscola():
    with pytest.raises(ValueError, match="PWD troppo corta"):
        valida_password("gattonemiagolo")

def test_password_numero():
    with pytest.raises (ValueError, match="PWD non ha numeri"):
        valida_password("Gattonemiagoloso")