import pytest
from banca import ContoBancario

def test_deposito_corretto():
    conto = ContoBancario("Mario", 100)
    conto.deposita(50)
    assert conto.saldo == 150

def test_prelievo_applica_commissione():
    conto = ContoBancario("Mario", 100)
    # Prelevo 50. Costo 50 + 2 (commissione) = 52. Saldo atteso: 48.
    conto.preleva(50)
    assert conto.saldo == 48

def test_hackeraggio_prelievo_negativo():
    conto = ContoBancario("Mario", 100)
    # Provo a prelevare un importo negativo per rubare soldi alla banca
    with pytest.raises(ValueError, match="L'importo deve essere positivo"):
        conto.preleva(-100)

def test_prelievo_fondi_insufficienti():
    conto = ContoBancario("Mario", 100)
    # Prelevo 100 + 2 commissione = 102. Deve fallire.
    with pytest.raises(ValueError, match="Fondi insufficienti"):
        conto.preleva(100)

def test_precisione_virgola_mobile():
    conto = ContoBancario("Mario", 0.1)
    conto.accredita_interessi(0.2)
    # Nelle banche i centesimi contano. Deve essere ESATTAMENTE 0.3, non 0.30000004
    assert conto.saldo == 0.3

def test_bonifico_fallito_rollback_sicuro():
    conto_mittente = ContoBancario("Mario", 100)
    conto_destinatario = ContoBancario("Luigi", 50)
    
    # Provo a fare un bonifico negativo (errore).
    with pytest.raises(ValueError):
        conto_mittente.bonifico(conto_destinatario, -10)
        
    # Se il bonifico fallisce, i soldi del mittente NON DEVONO SPARIRE.
    # Il saldo deve rimanere 100.
    assert conto_mittente.saldo == 100, "I soldi del mittente sono spariti nel nulla!"