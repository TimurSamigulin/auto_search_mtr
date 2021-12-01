"""
    Абстрактный класс для классов парсинга поисковиков
"""

from abc import ABC, abstractmethod


class Search(ABC):
    """Класс для поисковиков"""

    @abstractmethod
    def get_urls(self, q: str, start: int = 0):
        pass
