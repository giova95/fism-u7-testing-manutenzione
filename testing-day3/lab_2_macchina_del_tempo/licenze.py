import datetime

def licenza_scaduta(data_scadenza: str) -> bool:
    """Ritorna True se la licenza è scaduta rispetto a OGGI.
    Formato data: 'YYYY-MM-DD'
    """
    scadenza = datetime.datetime.strptime(data_scadenza, "%Y-%m-%d")
    oggi = datetime.datetime.now()
    
    return oggi > scadenza