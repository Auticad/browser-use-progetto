# src/tools.py
import json
from datetime import datetime
from pathlib import Path

from browser_use import Tools

tools = Tools()


@tools.action(
    description="Salva dati estratti in un file JSON nella cartella risultati"
)
def salva_json(nome_file: str, dati: dict) -> str:
    """Salva i dati in formato JSON con timestamp nel nome file."""
    output = Path("risultati")
    output.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output / f"{nome_file}_{ts}.json"
    path.write_text(json.dumps(dati, indent=2, ensure_ascii=False))
    return f"Salvato in {path}"


@tools.action(description="Leggi un file di testo dal disco e restituisci il contenuto")
def leggi_file(percorso: str) -> str:
    """Legge e restituisce il contenuto di un file .txt o .csv."""
    p = Path(percorso)
    if not p.exists():
        return f"ERRORE: file {percorso} non trovato"
    return p.read_text(encoding="utf-8")
