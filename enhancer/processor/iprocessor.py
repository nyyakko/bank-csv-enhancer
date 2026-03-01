from abc import ABC, abstractmethod

class IProcessor(ABC):
    @abstractmethod
    def process(self, csvFile):
        pass
