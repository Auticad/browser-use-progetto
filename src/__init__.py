"""
browser_use_progetto — Toolkit per agenti browser con browser-use.

API pubblica del pacchetto:

    crea_browser_persistente  factory per Browser con profilo persistente
    esegui_task               wrapper async per eseguire qualsiasi task
    tools                     registro delle azioni custom disponibili all'agente
    salva_json                salva un dict in JSON con timestamp in risultati/
    leggi_file                legge un file .txt/.csv dal disco
"""

from .agents import crea_browser_persistente, esegui_task
from .tools import leggi_file, salva_json, tools

__all__ = [
    "crea_browser_persistente",
    "esegui_task",
    "tools",
    "salva_json",
    "leggi_file",
]

__version__ = "0.1.0"
__author__ = "Pietro Cammise"
