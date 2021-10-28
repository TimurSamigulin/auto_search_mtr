from abc import ABC, abstractmethod, ABCMeta


class Search(ABC):

    @abstractmethod
    def get_urls(self, q: str, start: int = 0):
        pass
