import os

def carica_blacklist() -> list[str]:
    """Carica la blacklist da file, ritorna lista di password compromesse."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "blacklist.txt"), 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []