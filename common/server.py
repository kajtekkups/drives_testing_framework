
from abc import ABC, abstractmethod
from common.data_classes import Connectionstatus

class ServerInstance(ABC):
    @property
    @abstractmethod
    def get_connection_status(self) -> Connectionstatus:
        ...

    @classmethod
    @abstractmethod
    def initialize(self):
        ...
       
