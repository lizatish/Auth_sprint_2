# Репозиторий для работы

https://github.com/lizatish/Auth_sprint_2

# Развертка приложения

Для работы сервиса авторизации необходимо запустить контейнеры из docker-compose.yaml

```
docker-compose build
docker-compose up
```

Для запуска приложения в корне необходимо положить файл со скрытыми конфигами `.env`, заполненный значениями переменных:

```
MAIN_POSTGRES_DB_USER - имя пользователя для бд сервиса кинотеатра
MAIN_POSTGRES_DB_PASSWORD - пароль для бд сервиса кинотеатра
MAIN_POSTGRES_DB_NAME - имя бд сервиса кинотеатра 
MAIN_POSTGRES_DB_PORT - порт для бд сервиса кинотеатра
MAIN_POSTGRES_DB_HOST - имя хоста бд для сервиса кинотеатра

MAIN_ELASTIC_HOST - имя хоста elasticsearch
ELASTIC_URL - полный путь до elasticsearch (для etl)

AUTH_POSTGRES_DB_USER - имя пользователя для бд сервиса авторизации
AUTH_POSTGRES_DB_PASSWORD - пароль для бд сервиса авторизации
AUTH_POSTGRES_DB_NAME - имя бд сервиса авторизации 
AUTH_POSTGRES_DB_PORT - порт для бд сервиса авторизации
AUTH_POSTGRES_DB_HOST - имя хоста бд для сервиса автризации

SECRET_KEY - секретный ключ flask приложения
SQLALCHEMY_DATABASE_URI - полный путь к основной бд (для sqlalchemy)
AUTH_HASH_METHOD - метод для хеширования токенов
AUTH_HASH_SALT_LENGTH - длина соли для хеширования токенов
```

# Сваггер
Сваггер развернут по урлу:
http://auth_service:5555/apidocs/#/

Обратившись к порту 80, запросы будут отправляться в сервис авторизации.

# Тестирование

Тесты запускаются автоматически набором следующих команд:

```
cd tests/functional
docker-compose build
docker-compose up
```

Для запуска тестов в `tests/functional` необходимо положить файл со скрытыми конфигами `.env`, заполненный значениями
переменных:

```
CACHE_HOST - порт бд для кеширования

POSTGRES_DB_NAME - имя основной бд (postgres)
POSTGRES_DB_PASSWORD - пароль основной бд
POSTGRES_DB_USER - имя пользователя основной бд
SQLALCHEMY_DATABASE_URI - полный путь к основной бд (для sqlalchemy)

AUTH_HASH_METHOD - метод для хеширования токенов
AUTH_HASH_SALT_LENGTH - длина соли для хеширования токенов
```

# Над проектом работали:
1. Тишковец Елизавета
   - авторизация (Twitter, Yandex)
   - подключение Jaeger
   - интеграция с AsyncAPI
2. Рубцов Олег
   - авторизация (Google, Facebook)
   - ограничение количества запросов к серверу (Rate limit)
   - партицирование в PostgreSQL
