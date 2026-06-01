# esempi/test_env.py — verifica configurazione .env
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

openai_key = os.getenv("OPENAI_API_KEY", "")
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

if openai_key:
    print(f"OPENAI_API_KEY trovata:    ...{openai_key[-6:]}")
else:
    print("OPENAI_API_KEY:    non configurata")

if anthropic_key:
    print(f"ANTHROPIC_API_KEY trovata: ...{anthropic_key[-6:]}")
else:
    print("ANTHROPIC_API_KEY: non configurata")

if not openai_key and not anthropic_key:
    print("\nERRORE: nessuna chiave API trovata. Controlla il file .env")
    raise SystemExit(1)
else:
    print("\nConfigurazione OK.")
