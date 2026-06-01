# primo_agente.py
import asyncio

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

# Carica le variabili da .env (OPENAI_API_KEY)
load_dotenv()


async def main():
    # Inizializza il modello OpenAI tramite il wrapper nativo di browser-use
    llm = ChatOpenAI(model="gpt-4o")

    task = """Vai su wikipedia.org, trova il titolo dell'articolo in evidenza
    oggi nella homepage e restituiscilo come risultato finale."""

    agent = Agent(task=task, llm=llm)
    history = await agent.run()

    print("\n--- RISULTATO FINALE ---")
    result = history.final_result()

    if result:
        print(result)
    else:
        contents = history.extracted_content()
        if contents:
            print(contents[-1])
        else:
            print("Nessun contenuto estratto.")


if __name__ == "__main__":
    asyncio.run(main())
