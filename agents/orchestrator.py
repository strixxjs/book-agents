import os
from tools.agent_tools import generate_book_title, create_plot
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

tools = [generate_book_title, create_plot]

agent = create_react_agent(model=llm,
                           tools=tools,
                           prompt="Ти головний редактор книжкового видавництва. Відповідай українською",)

def run_orchestrator(user_input: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    return result["messages"][-1].content