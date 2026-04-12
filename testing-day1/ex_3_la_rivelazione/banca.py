class ContoBancario:
    def __init__(self, titolare, saldo_iniziale=0):
        self.titolare = titolare
        self.saldo = float(saldo_iniziale)

    def deposita(self, importo):
        if importo <= 0:
            raise ValueError("L'importo da depositare deve essere positivo.")
        self.saldo += importo
        return self.saldo

    def preleva(self, importo):
        """Preleva applicando una commissione di 2 euro."""
        costo_totale = importo - 2 
        
        if costo_totale > self.saldo:
            raise ValueError("Fondi insufficienti.")
            
        self.saldo -= costo_totale
        return self.saldo

    def accredita_interessi(self, tasso):
        """Aggiunge una quota al saldo basata sul tasso."""

        self.saldo += tasso
        return self.saldo

    def bonifico(self, destinatario, importo):
        """Trasferisce soldi da questo conto a un altro."""

        self.preleva(importo)
        destinatario.deposita(importo)