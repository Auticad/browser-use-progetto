# src/agents.py
from browser_use import Agent, Browser, ChatOpenAI
from browser_use.browser.profile import BrowserProfile

from .config import (
    DEFAULT_MAX_ACTIONS_PER_STEP,
    DEFAULT_MAX_STEPS,
    DEFAULT_MODEL,
    PROFILI_DIR,
)


def crea_browser_persistente(nome_profilo: str = "profilo_default") -> Browser:
    """
    Crea un browser con profilo persistente.
    I cookie e le sessioni vengono mantenuti tra le esecuzioni.

    Args:
        nome_profilo: nome della sottocartella in profili/ dove salvare il profilo.

    Returns:
        Istanza Browser configurata con profilo persistente.
    """
    profilo_path = PROFILI_DIR / nome_profilo
    profilo_path.mkdir(parents=True, exist_ok=True)

    profile = BrowserProfile(
        headless=False,  # True per esecuzione silenziosa
        user_data_dir=str(profilo_path),
        viewport={"width": 1280, "height": 900},
        locale="it-IT",
    )
    return Browser(browser_profile=profile)


async def esegui_task(task: str, browser: Browser | None = None) -> str:
    """
    Wrapper riutilizzabile per eseguire qualsiasi task.

    Args:
        task:    descrizione in linguaggio naturale di cosa deve fare l'agente.
        browser: istanza Browser opzionale (usa il default se None).

    Returns:
        Risultato finale restituito dall'agente, o stringa vuota.
    """
    llm = ChatOpenAI(model=DEFAULT_MODEL)

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        max_actions_per_step=DEFAULT_MAX_ACTIONS_PER_STEP,
    )
    history = await agent.run(max_steps=DEFAULT_MAX_STEPS)
    return history.final_result() or ""
