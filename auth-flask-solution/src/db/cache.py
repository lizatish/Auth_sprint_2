from abc import abstractmethod, ABC


class CacheStorage(ABC):
    """Абстрактный класс для кеша."""

    @abstractmethod
    def get(self, key: str, **kwargs) -> str:
        """Возвращает элементы по ключу.

         Args:
            key: ключ
            kwargs: доп. параметры

        Returns:
            str: элементы по ключу
        """
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int, **kwargs) -> str:
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
    def lrange(self, key: str, start: int, stop: int, **kwargs) -> list:
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
    def lpush(self, key: str, *elements: list[str], **kwargs) -> int:
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
    def expire(self, key: str, seconds: int, **kwargs) -> bool:
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
    def close(self):
        """Закрывает соединение."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Удаляет данные по ключу."""
        pass

    @abstractmethod
    def keys(self, condition: str) -> list[str]:
        """Возвращает все ключи, удовлетворяюще условию."""
        pass
