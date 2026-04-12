import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import PlotOutline

load_dotenv()

def run_plot_agent(topic: str, genre: str) -> PlotOutline:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    system_prompt = SystemMessage(content=(
        "Ви — професійний сценарист та письменник. "
        "Ваше завдання — створювати структуровані сюжети для книг. "
        "Ви повинні відповідати ТІЛЬКИ валідним JSON-об'єктом, без жодного вступного чи завершального тексту. "
        "Структура JSON має бути такою:\n"
        "{\n"
        "  \"title\": \"назва книжки\",\n"
        "  \"synopsis\": \"короткий опис сюжету\",\n"
        "  \"characters\": [\"персонаж 1\", \"персонаж 2\"],\n"
        "  \"chapters_plan\": [\"розділ 1\", \"розділ 2\", \"розділ 3\"]\n"
        "}"
    ))

    human_message = HumanMessage(content=(f"Створю сюжет для книжки. Тема: {topic}. Жанр: {genre}"))

    response = llm.invoke([system_prompt, human_message])

    content = response.content.strip()
    if content.startswith("```json"):
        content = content.replace("```json", "", 1).replace("```", "", 1).strip()
    elif content.startswith("```"):
        content = content.replace("```", "", 1).replace("```", "", 1).strip()

    parsed_json = json.loads(content)
    return PlotOutline(**parsed_json)