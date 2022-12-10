from abc import ABC, abstractmethod
from typing import Dict

from src.database import Session


class API(ABC):
    @abstractmethod
    def _build_url(self) -> str:
        pass

    @abstractmethod
    def call_endpoint(self) -> Dict:
        pass

    def save_to_db(self, table) -> None:
        data = self.call_endpoint()
        raw_metric = table(data=data)

        session = Session()
        session.add(raw_metric)
        session.commit()
