# Demo avanzata — API del pacchetto `src`

Questo script mostra come usare in combinazione tutte le componenti di `src/`: browser persistente, tool custom passati all'agente, lettura da file, salvataggio JSON.

**Scenario:** una pipeline che legge una lista di termini da un file `.txt`, li cerca su Wikipedia uno per uno, e chiede all'agente di salvare ogni risultato tramite lo strumento `salva_json` registrato in `src/tools.py`.

---

## Cosa viene usato e perché

| Componente | Provenienza | Ruolo nello script |
|-----------|------------|-------------------|
| `crea_browser_persistente` | `src/agents.py` | Browser con profilo riutilizzabile — la sessione sopravvive tra le run |
| `tools` | `src/tools.py` | Registro delle azioni passato all'agente — decide autonomamente quando salvarle |
| `leggi_file` | `src/tools.py` | Legge la lista di termini da file senza duplicare logica I/O |
| `salva_json` | `src/tools.py` | Usato direttamente nello script per il riepilogo finale |

---

## Script

Salva questo file come `esempi/pipeline_ricerca.py` e rieseguilo ogni volta che vuoi aggiornare la lista dei termini.

```python
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
            "Intelligenza artificiale\n"
            "Large Language Model\n"
            "Browser automation\n",
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
             nome_file = "{termine.lower().replace(' ', '_')}"
             dati      = {{"termine": "{termine}", "titolo": "...", "paragrafo": "...", "categoria": "..."}}
        6. Restituisci il percorso del file salvato come risultato finale.
        """

        # 3. Agent con tools: l'agente può chiamare salva_json e leggi_file
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            tools=tools,          # <── tool registry da src/tools.py
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
```

---

## Come eseguirlo

```bash
# Crea/modifica prima il file dei termini (uno per riga)
echo -e "Reti neurali\nReinforcement learning\nTransformer" > termini_ricerca.txt

# Avvia la pipeline
python esempi/pipeline_ricerca.py
```

I file JSON vengono salvati in `risultati/` con timestamp nel nome. Il browser riusa il profilo `profili/ricerca_wiki/` tra le esecuzioni successive: se Wikipedia ha già una sessione aperta, la mantiene.

---

## Estendere la pipeline

**Aggiungere un nuovo tool** — basta decorare una funzione in `src/tools.py`:

```python
@tools.action(description="Invia una notifica su stdout con timestamp")
def notifica(messaggio: str) -> str:
    from datetime import datetime
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {messaggio}")
    return f"Notifica inviata alle {ts}"
```

Il tool sarà disponibile all'agente nella prossima esecuzione senza modifiche allo script.

**Cambiare il modello o i parametri** — modifica `.env` senza toccare il codice:

```
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_MAX_STEPS=15
```
