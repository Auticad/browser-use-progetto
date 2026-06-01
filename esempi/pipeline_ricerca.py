# esempi/pipeline_ricerca.py
"""
Pipeline di ricerca Wikipedia che usa l'intera API di src/:
  - leggi_file        carica i termini dal file di input
  - crea_browser_persistente  browser con sessione mantenuta tra le run
  - tools             passa le azioni custom all'agente
  - salva_json        usato sia dall'agente che direttamente nello script
"""

import asyncio
from pathlib import Path

from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

from src import crea_browser_persistente, leggi_file, salva_json, tools

load_dotenv()

# ── Configurazione ────────────────────────────────────────────────────────────
TERMINI_PATH = "termini_ricerca.txt"
PROFILO_BROWSER = "ricerca_wiki"


def prepara_file_input() -> None:
    """Crea il file di input con termini di esempio se non esiste già."""
    p = Path(TERMINI_PATH)
    if not p.exists():
        p.write_text(
            "Intelligenza artificiale\nLarge Language Model\nBrowser automation\n",
            encoding="utf-8",
        )
        print(f"Creato {TERMINI_PATH} con termini di esempio.")


# ── Pipeline principale ───────────────────────────────────────────────────────
async def main() -> None:
    prepara_file_input()

    # 1. leggi_file: carica e analizza i termini dal file di testo
    contenuto = leggi_file(TERMINI_PATH)
    termini = [t.strip() for t in contenuto.splitlines() if t.strip()]
    print(f"Termini da cercare ({len(termini)}): {termini}\n")

    # 2. crea_browser_persistente: il profilo mantiene cookie e sessioni
    browser = crea_browser_persistente(PROFILO_BROWSER)
    llm = ChatOpenAI(model="gpt-4o")

    riepilogo = []

    for termine in termini:
        print(f"→ {termine}")

        task = f"""
        1. Vai su https://it.wikipedia.org
        2. Cerca nella barra di ricerca: {termine}
        3. Apri il primo risultato pertinente
        4. Estrai le seguenti informazioni:
             - titolo:     il titolo esatto della pagina Wikipedia
             - paragrafo:  il primo paragrafo del corpo dell'articolo
             - categoria:  la categoria principale in fondo alla pagina
        5. Chiama lo strumento salva_json con:
             nome_file = "{termine.lower().replace(" ", "_")}"
             dati      = {{"termine": "{termine}", "titolo": "...", "paragrafo": "...", "categoria": "..."}}
        6. Restituisci il percorso del file salvato come risultato finale.
        """

        # 3. Agent con tools: l'agente può chiamare salva_json e leggi_file
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            tools=tools,  # <── tool registry da src/tools.py
            max_actions_per_step=5,
        )
        history = await agent.run(max_steps=20)
        output = history.final_result() or "nessun risultato"
        riepilogo.append({"termine": termine, "file_salvato": output})
        print(f"   {output}\n")

    # 4. salva_json: usato direttamente (non tramite agente) per il riepilogo
    path_riepilogo = salva_json("riepilogo_pipeline", {"ricerche": riepilogo})
    print(f"Riepilogo finale salvato in: {path_riepilogo}")

    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
