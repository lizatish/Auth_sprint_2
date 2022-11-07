from abc import ABC, abstractmethod


class AsyncSearchEngine(ABC):
    """Абстрактный класс, реализующий работу поискового движка."""

    @abstractmethod
    def __init__(self, **kwargs):
        """Инициализирует поисковой движок."""
        pass

    @abstractmethod
    async def close(self, **kwargs):
        """Закрывает соединение с движком.."""
        pass

    @abstractmethod
    async def search(
            self,
            index: str,
            from_: int = None,
            size: int = None,
            body: dict = None,
            **kwargs,
    ):
        """Производит поиск документов."""
        pass

    @abstractmethod
    async def get(self, index: str, id: str, **kwargs) -> dict:
        """Возвращает документ заданного индекса по идентификатору."""
        pass
