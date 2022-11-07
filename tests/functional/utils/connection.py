import logging
import time
import typing
from functools import wraps

_TException = typing.TypeVar('_TException', bound=Exception)

logger = logging.getLogger()


def sync_backoff(
        occurred_exception: typing.Type[_TException],
        backoff_logger: logging.Logger = logger,
        tries=20,
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
) -> typing.Callable:
    """Функция для повторного выполнения через некоторое время.

    Args:
        :occurred_exception: возникшая ошибка
        :logger: начальное время повтора
        :tries: начальное время повтора
        :start_sleep_time: начальное время повтора
        :factor: во сколько раз нужно увеличить время ожидания
        :border_sleep_time: граничное время ожидания

    Returns:
        typing.Callable: Результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            mtries, mdelay = tries, start_sleep_time
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except occurred_exception as ex:
                    ex_str = str(ex).strip()
                    backoff_logger.exception(f'{ex_str}')
                    backoff_logger.exception(
                        f'Retrying in {mdelay} seconds...\n',
                    )

                    time.sleep(mdelay)
                    mtries -= 1

                    if mdelay < border_sleep_time:
                        mdelay *= 2 ** factor
                    if mdelay >= border_sleep_time:
                        mdelay = border_sleep_time
            return occurred_exception

        return inner

    return func_wrapper


def async_backoff(
        *occurred_exceptions: [typing.Type[_TException]],
        backoff_logger: logging.Logger = logger,
        tries=20,
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
) -> typing.Callable:
    """Функция для повторного выполнения через некоторое время.

    Args:
        :occurred_exception: возникшая ошибка
        :logger: начальное время повтора
        :tries: начальное время повтора
        :start_sleep_time: начальное время повтора
        :factor: во сколько раз нужно увеличить время ожидания
        :border_sleep_time: граничное время ожидания

    Returns:
        typing.Callable: Результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            mtries, mdelay = tries, start_sleep_time
            while mtries > 1:
                try:
                    await func(*args, **kwargs)
                    break
                except occurred_exceptions as ex:
                    ex_str = str(ex).strip()
                    backoff_logger.exception(f'{ex_str}')
                    backoff_logger.exception(
                        f'Retrying in {mdelay} seconds...\n',
                    )

                    time.sleep(mdelay)
                    mtries -= 1

                    if mdelay < border_sleep_time:
                        mdelay *= 2 ** factor
                    if mdelay >= border_sleep_time:
                        mdelay = border_sleep_time

            return occurred_exceptions

        return inner

    return func_wrapper
