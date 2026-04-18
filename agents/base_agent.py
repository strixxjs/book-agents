from abc import ABC, abstractmethod
from utils.decorators import timer

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        pass

    def log(self, message: str):
        print(f"[{self.name}]: {message}")

    def validate_input(self, input_data: dict) -> bool:
        if not input_data:
            return False
        return True

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"

    def __str__(self):
        return f"Agent: {self.name}"


class WriterAgent(BaseAgent):
    @timer
    def run(self, input_data: dict) -> dict:
        self.log("Starting...")
        if not self.validate_input(input_data):
            raise ValueError
        else:
            return {"result": "Writing chapter..."}


agent = WriterAgent("Writer")
print(agent.run({"topic": "Chapter 1"}))
print(agent.run({}))