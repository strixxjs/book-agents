import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import PlotOutline, Chapter

load_dotenv()

def run_chapter_agent(plot: PlotOutline, chapter_title: str, chapter_number: int) -> Chapter:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.8,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    system_prompt = SystemMessage(content = ("Ви — талановитий письменник-фантаст. Ваше завдання — написати повний текст конкретного розділу книги. "
        "Пишіть художньо, з описами та діалогами. Текст розділу повинен містити мінімум 3 розгорнуті абзаци. "
        "Ви повинні повернути ТІЛЬКИ валідний JSON без жодного додаткового тексту:\n"
        "{\n"
        "  \"number\": 1,\n"
        "  \"title\": \"назва розділу\",\n"
        "  \"content\": \"повний текст розділу...\"\n"
        "}"
                                             ))

    human_content = (
        f"Назва книжки: {plot.title}\n"
        f"Персонажі: {', '.join(plot.characters)}\n"
        f"Загальний сюжет: {plot.synopsis}\n\n"
        f"Напиши розділ #{chapter_number}: {chapter_title}"
    )

    human_message = HumanMessage(content=human_content)

    response = llm.invoke([system_prompt, human_message])

    content = response.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1).replace("```", "", 1).strip()
    elif content.startswith("```"):
        content = content.replace("```", "", 1).replace("```", "", 1).strip()

    parsed_json = json.loads(content)
    return Chapter(**parsed_json)