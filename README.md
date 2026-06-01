# browser-use-progetto

Toolkit di partenza per costruire agenti browser con [browser-use](https://github.com/browser-use/browser-use) e modelli OpenAI. Il repository fornisce una struttura modulare riutilizzabile, esempi progressivi e un set di tool custom per interagire con il filesystem.

---

## About

**Autore:** [Pietro Cammise](https://github.com/Auticad) — AI/ML Engineer  
**Portfolio:** [auticad.github.io/cv_cammise](https://auticad.github.io/cv_cammise/)  
**Stack:** Python 3.11+, browser-use ≥ 0.12.6, GPT-4o  


browser-use è una libreria Python che trasforma un LLM in un agente capace di controllare un browser reale: navigare pagine, compilare form, estrarre dati strutturati — senza Selenium, senza scraping manuale, senza XPath. L'agente percepisce la pagina come un albero di elementi accessibili e decide autonomamente quali azioni compiere per completare il task assegnato in linguaggio naturale.

Questo repository nasce come base di studio pratica: ogni modulo ha uno scopo preciso, gli esempi sono progressivi, e la configurazione è centralizzata per evitare valori hardcodati sparsi nel codice.

---

## Struttura del progetto

```
browser_use_progetto/
├── src/
│   ├── __init__.py          # API pubblica del pacchetto
│   ├── agents.py            # Factory e wrapper per agenti browser-use
│   ├── config.py            # Configurazione centralizzata (env + percorsi)
│   └── tools.py             # Tool custom: salva_json, leggi_file
├── esempi/
│   ├── primo_agente.py      # Agente minimale: recupera titolo da Wikipedia
│   ├── ricerca_dati.py      # Ricerca con estrazione strutturata
│   ├── compila_form.py      # Compilazione automatica di un form HTML
│   ├── navigazione_multi.py # Estrazione da Hacker News + salvataggio JSON
│   └── test_env.py          # Verifica configurazione .env
├── risultati/               # Output JSON generati (gitignored)
├── profili/                 # Profili browser persistenti (gitignored)
├── .env.example             # Template variabili d'ambiente
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clona il repository

```bash
git clone https://github.com/Auticad/browser-use-progetto.git
cd browser-use-progetto
```

### 2. Crea l'ambiente virtuale

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

> browser-use scarica automaticamente Playwright e Chromium al primo avvio.
> Se non avviene, esegui manualmente: `playwright install chromium`

### 4. Configura le variabili d'ambiente

```bash
cp .env.example .env
```

Apri `.env` e inserisci la tua chiave OpenAI:

```
OPENAI_API_KEY=sk-proj-...
```

Verifica che tutto funzioni:

```bash
python esempi/test_env.py
```

---

## Utilizzo

### Agente minimale (standalone)

```python
import asyncio
from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

async def main():
    llm = ChatOpenAI(model="gpt-4o")
    agent = Agent(
        task="Vai su wikipedia.org e dimmi il titolo dell'articolo in evidenza.",
        llm=llm
    )
    history = await agent.run()
    print(history.final_result())

asyncio.run(main())
```

### Usare il pacchetto `src`

```python
import asyncio
from src import esegui_task, crea_browser_persistente

async def main():
    # Browser con profilo persistente: cookie e sessioni sopravvivono ai riavvii
    browser = crea_browser_persistente("mio_profilo")
    risultato = await esegui_task(
        task="Vai su news.ycombinator.com e dimmi il titolo del primo articolo.",
        browser=browser,
    )
    print(risultato)

asyncio.run(main())
```

### Tool custom

`src/tools.py` registra due azioni che l'agente può chiamare autonomamente durante l'esecuzione:

| Tool | Firma | Descrizione |
|------|-------|-------------|
| `salva_json` | `(nome_file: str, dati: dict) → str` | Salva un dict come file JSON con timestamp in `risultati/` |
| `leggi_file` | `(percorso: str) → str` | Legge un file `.txt` o `.csv` e ne restituisce il contenuto |

Per aggiungere un tool, decorare una funzione con `@tools.action(description="...")` in `src/tools.py`.

---

## Esempi

| File | Cosa fa |
|------|---------|
| `primo_agente.py` | Punto di partenza: un agente, un task, un risultato |
| `ricerca_dati.py` | Ricerca su Wikipedia con estrazione di titolo, paragrafo e categoria |
| `compila_form.py` | Naviga su httpbin.org e compila un form HTML reale step by step |
| `navigazione_multi.py` | Scraping da Hacker News con salvataggio automatico su file JSON |

```bash
# Eseguire un esempio
python esempi/primo_agente.py
python esempi/navigazione_multi.py
```

---

## Configurazione avanzata

I parametri si controllano tramite variabili d'ambiente in `.env`. Tutti i valori hanno un default sensato e sono opzionali tranne la chiave API.

| Variabile | Default | Descrizione |
|-----------|---------|-------------|
| `OPENAI_API_KEY` | — | Chiave API OpenAI (**obbligatoria** se non si usa Anthropic) |
| `ANTHROPIC_API_KEY` | — | Chiave API Anthropic (alternativa a OpenAI) |
| `DEFAULT_MODEL` | `gpt-4o` | Modello LLM usato dagli agenti |
| `DEFAULT_MAX_STEPS` | `30` | Step massimi per esecuzione agente |
| `DEFAULT_MAX_ACTIONS_PER_STEP` | `5` | Azioni massime per step |

`src/config.py` carica e valida queste variabili all'import. Se nessuna chiave API è presente, solleva `EnvironmentError` immediatamente, prima che l'agente tenti di connettersi.

---

## Architettura

```
.env
 └─► src/config.py          carica env, definisce costanti e crea directory
      ├─► src/agents.py     usa DEFAULT_MODEL, DEFAULT_MAX_STEPS, PROFILI_DIR
      └─► src/tools.py      indipendente, registra le azioni custom

src/__init__.py              espone l'API pubblica del pacchetto
```

Il flusso è volutamente piatto: un solo punto di ingresso per la configurazione, zero dipendenze circolari, nessun valore hardcodato nei moduli.

---

## Dipendenze

| Pacchetto | Versione minima | Scopo |
|-----------|----------------|-------|
| `browser-use` | ≥ 0.12.6 | Runtime agenti browser |
| `anthropic` | ≥ 0.40.0 | SDK Anthropic (uso opzionale) |
| `python-dotenv` | ≥ 1.0.0 | Caricamento `.env` |
| `pydantic` | ≥ 2.0.0 | Validazione schema dei tool |

**Requisito Python:** ≥ 3.11 (necessario per la sintassi `X | Y` nei type hint).

---

## Note e limitazioni

- Il browser si apre in modalità visibile (`headless=False`) di default per facilitare il debug. Impostare `headless=True` in `src/agents.py` per esecuzione in background.
- I profili browser (cookie, sessioni autenticate) vengono salvati in `profili/` e non sono versionati: utili per mantenere sessioni attive tra esecuzioni diverse.
- I tool custom usano l'API `Tools()` di browser-use. L'API potrebbe variare nelle versioni future della libreria: verificare le release notes prima di aggiornare.
- Il file `.env` non deve mai essere committato. È già in `.gitignore`, ma è buona norma verificarlo prima di ogni push con `git status`.

---

This project is licensed under the [MIT License](LICENSE)