# API AIOHTTP
REST API приложение

## Установка и запуск

```sh
git clone https://github.com/makivila/simaland_test.git
cd simaland_test
make run
make migrate_up

```

В приложении по умолчанию заведен admin пользователь с логином admin и паролем password.

## Доступные команды
Доступ к логам:

```sh
make logs

```

Остановить приложение:

```sh
make stop

```

Апгрейд миграции:

```sh
make migrate_revision
make migrate_up

```

Даунгрейд миграции:

```sh
make migrate_down

```

## Выполненные задачи

- CRUD на таблицы Users и Roles

- Управление сессиями

- Возможность администратору выполнять любой метод, а пользователю только со своей учетной записью

- Настроенные разрешения к методам API, которые можно редактировать в базе или API-методом обновления роли

- Логирование ошибок

- Миграции через Alembic

- Docker-compose и Makefile



# Документация API


### AUTH

Авторизация

При успешной авторизации задает сессию в cookie
```sh
POST /api/v1/auth/login
body:
{
    "login": "john_titor",
    "password": "super_password"
}
```

Регистрация нового пользователя

Регистрация нового администратора доступна только другим администраторам
```sh
POST /api/v1/auth/register
body:
{
    "first_name": "john",
    "second_name": "titor",
    "login": "john_titor",
    "password": "password",
    "role": "user",
    "born": "2000-06-24"
}
```

### USERS

Получение всех пользователей
```sh
GET /api/v1/users/
```

Получение пользователя по ID
```sh
GET /api/v1/users/{id}
```

Обновление пользователя
```
PUT /api/v1/users/{id}
body:
{
    "first_name": "john",
    "second_name": "titor",
    "login": "john_titor",
    "password": "password",
    "role": "user",
    "born": "2000-06-24"
}
```

Удаление пользователя
```sh
DELETE /api/v1/users/{id}
```

### ROLES

Создание новой роли
```sh
POST /api/v1/roles/
body:
{
    "role": "vip_user",
    "permissions": ["get_all_users", "get_all_roles"]
}
```

Получение всех ролей
```sh
GET /api/v1/roles/
```

Получение роли по ID
```sh
GET /api/v1/roles/{id}
```

Обновление роли
```sh
PUT /api/v1/roles/{id}
body:
{
    "role": "super_vip_user",
    "permissions": ["get_all_users", "get_all_roles"]
}
```

Удаление роли
```sh
DELETE /api/v1/roles/{id}
```
