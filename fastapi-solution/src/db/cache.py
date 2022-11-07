from abc import abstractmethod, ABC


class AsyncCacheStorage(ABC):
    """Абстрактный класс для кеша."""

    @abstractmethod
    async def get(self, key: str, **kwargs) -> str:
        """Возвращает элементы по ключу.

         Args:
            key: ключ
            kwargs: доп. параметры

        Returns:
            str: элементы по ключу
        """
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs) -> str:
        """Записывает ключ для хранения значения.

         Args:
            key: ключ
            value: значение
            expire: время актуальности данных
            kwargs: доп. параметры

        Returns:
            str: строковое представление результата операции
        """
        pass

    @abstractmethod
    async def lrange(self, key: str, start: int, stop: int, **kwargs) -> list:
        """Возвращает диапазон значений, лежащих по ключу.

        Args:
            key: ключ
            start: начальное смещение
            stop: конечное смещение
            kwargs: доп. параметры

        Returns:
            list: список элементов, попавших в диапазон
        """
        pass

    @abstractmethod
    async def lpush(self, key: str, *elements: list[str], **kwargs) -> int:
        """Кладет элемент в список по ключу в начало очереди.

        Args:
            key: ключ
            elements: значение элемента
            kwargs: доп. параметры

        Returns:
            int: размер списка по ключу после вставки
        """
        pass

    @abstractmethod
    async def expire(self, key: str, seconds: int, **kwargs) -> bool:
        """Задает время, после которого ключ станет невалидным.

        Args:
            key: ключ
            seconds: количество секунд
            kwargs: доп. параметры

         Returns:
            bool: результат выполнения операции
        """
        pass

    @abstractmethod
    async def close(self):
        """Закрывает соединение."""
        pass
