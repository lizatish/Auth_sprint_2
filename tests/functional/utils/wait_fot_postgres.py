import psycopg2
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import DictCursor

from tests.functional.logger import get_logger
from tests.functional.settings import get_settings
from tests.functional.utils.connection import sync_backoff

conf = get_settings()
logger = get_logger()


@sync_backoff(psycopg2.OperationalError, backoff_logger=logger)
def create_pg_connection(dsl: dict) -> pg_connection:
    """Создает соединение к postgresql.

    Args:
        dsl: Параметры соединения

     Returns:
        pg_connection: Соединение к postgresql
    """
    return psycopg2.connect(**dsl, cursor_factory=DictCursor)


def main():
    """Ожидает подключение к postgres."""
    dsl = {
        'dbname': conf.POSTGRES_DB_NAME,
        'user': conf.POSTGRES_DB_USER,
        'password': conf.POSTGRES_DB_PASSWORD,
        'host': conf.POSTGRES_DB_HOST,
        'port': conf.POSTGRES_DB_PORT,
    }
    connection = create_pg_connection(dsl)
    logger.debug('Connection to postgres established!')
    connection.close()


if __name__ == '__main__':
    main()
