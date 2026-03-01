from .transaction import Transaction

from abc import ABC, abstractmethod
from typing import List

class IProcessor(ABC):
    @abstractmethod
    def process(self, csvFile) -> List[Transaction]:
        pass

