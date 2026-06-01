# esempi/navigazione_multi.py
import asyncio
import json
from datetime import datetime
from pathlib import Path

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


async def raccogli_notizie() -> dict:
    llm = ChatOpenAI(model="gpt-4o")

    task = """
    1. Vai su https://news.ycombinator.com (Hacker News)
    2. Estrai i titoli e gli URL dei primi 5 articoli nella homepage
    3. Per ogni articolo annota il numero di punti e commenti
    4. Restituisci un JSON con questa struttura:
       {"articoli": [{"titolo": "...", "url": "...", "punti": 0, "commenti": 0}]}
    Restituisci SOLO il JSON, senza altro testo.
    """

    agent = Agent(task=task, llm=llm)
    history = await agent.run(max_steps=10)
    raw = history.final_result()

    try:
        dati = json.loads(raw)
    except json.JSONDecodeError:
        dati = {"raw": raw, "errore": "parsing JSON fallito"}

    # Salva su file con timestamp
    output_path = (
        Path("risultati") / f"notizie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(dati, indent=2, ensure_ascii=False))

    print(f"Risultati salvati in: {output_path}")
    return dati


if __name__ == "__main__":
    asyncio.run(raccogli_notizie())
