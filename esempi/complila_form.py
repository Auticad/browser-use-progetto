# esempi/compila_form.py
import asyncio

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


async def compila_form():
    llm = ChatOpenAI(model="gpt-4o")

    task = """
    1. Vai su https://httpbin.org/forms/post
    2. Compila il campo "Customer name" con "Mario Rossi"
    3. Compila "Telephone" con "02-12345678"
    4. Seleziona "Large" nella dimensione pizza
    5. Spunta il topping "Mushrooms"
    6. Fai click su "Submit order"
    7. Conferma che la pagina di risposta mostri i dati inseriti
    """

    agent = Agent(task=task, llm=llm)
    history = await agent.run(max_steps=20)
    print(history.final_result())


if __name__ == "__main__":
    asyncio.run(compila_form())
