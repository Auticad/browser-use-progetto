# esempi/ricerca_dati.py
import asyncio

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

# Carica le variabili da .env (OPENAI_API_KEY)
load_dotenv()


async def ricerca_dati(termine: str) -> str:
    # Wrapper nativo browser-use, NON langchain_openai
    llm = ChatOpenAI(model="gpt-4o")

    task = f"""
    1. Vai su https://it.wikipedia.org
    2. Cerca nella barra di ricerca il termine: {termine}
    3. Apri il primo risultato pertinente
    4. Estrai: titolo della pagina, primo paragrafo, e la categoria principale
    5. Restituisci queste informazioni come risultato finale in formato strutturato
    """

    agent = Agent(
        task=task,
        llm=llm,
        max_actions_per_step=4,
    )
    history = await agent.run(max_steps=15)

    result = history.final_result()

    if result:
        return result
    else:
        contents = history.extracted_content()
        if contents:
            return contents[-1]
        return "Nessun risultato estratto."


if __name__ == "__main__":
    risultato = asyncio.run(ricerca_dati("Intelligenza artificiale"))
    print("\n--- RISULTATO ---")
    print(risultato)
