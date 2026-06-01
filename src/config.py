"""
src/config.py — Configurazione centralizzata.

Carica variabili d'ambiente da .env e definisce costanti globali di percorso
e parametri agente. Tutti gli altri moduli importano da qui invece di
leggere os.environ direttamente.

Lancia EnvironmentError all'import se nessuna chiave API è configurata,
evitando errori silenziosi a runtime.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Carica .env dalla root del progetto (due livelli sopra questo file)
_ROOT = Path(__file__).parent.parent
load_dotenv(_ROOT / ".env")

# ── Chiavi API ───────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

if not OPENAI_API_KEY and not ANTHROPIC_API_KEY:
    raise EnvironmentError(
        "Nessuna chiave API trovata. "
        "Aggiungi OPENAI_API_KEY o ANTHROPIC_API_KEY nel file .env"
    )

# ── Parametri agente ─────────────────────────────────────────────────────────
DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o")
DEFAULT_MAX_STEPS: int = int(os.getenv("DEFAULT_MAX_STEPS", "30"))
DEFAULT_MAX_ACTIONS_PER_STEP: int = int(os.getenv("DEFAULT_MAX_ACTIONS_PER_STEP", "5"))

# ── Percorsi ─────────────────────────────────────────────────────────────────
ROOT_DIR: Path = _ROOT
RISULTATI_DIR: Path = ROOT_DIR / "risultati"
PROFILI_DIR: Path = ROOT_DIR / "profili"

# Crea le directory se non esistono (idempotente)
RISULTATI_DIR.mkdir(exist_ok=True)
PROFILI_DIR.mkdir(exist_ok=True)
