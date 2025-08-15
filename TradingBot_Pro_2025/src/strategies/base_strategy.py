from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.status = "STOPPED"

    @abstractmethod
    def execute(self):
        """
        Execute the trading strategy.
        """
        pass

    def start(self):
        """
        Start the trading strategy.
        """
        self.status = "RUNNING"
        print(f"Strategy {self.name} started.")

    def stop(self):
        """
        Stop the trading strategy.
        """
        self.status = "STOPPED"
        print(f"Strategy {self.name} stopped.")

    def get_status(self):
        """
        Get the status of the trading strategy.
        """
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status
        }
