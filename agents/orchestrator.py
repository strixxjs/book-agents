import os
from tools.agent_tools import generate_book_title, create_plot, create_chapter
from agents.base_agent import BaseAgent
from utils.decorators import timer
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

tools = [generate_book_title, create_plot, create_chapter]


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Orchestrator")
        self.agent = create_react_agent(model=llm,
                           tools=tools,
                           prompt="Ти головний редактор книжкового видавництва. Відповідай українською",)

    @timer
    def run(self, input_data: dict) -> dict:
        result = self.agent.invoke({"messages": [{"role": "user", "content": input_data}]})
        return result["messages"][-1].content