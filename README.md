# FastAPI Blog

REST API блога на FastAPI + SQLAlchemy + Alembic. Аутентификация на JWT,
конфигурация через `pydantic-settings`, логирование действий пользователя
в stdout, инфраструктура — Docker + PostgreSQL.

## Сущности

- `User` — пользователь и автор контента
- `Category` — категория публикации
- `Location` — локация публикации
- `Post` — публикация
- `Comment` — комментарий к публикации

## Конфигурация

Все параметры берутся из переменных окружения / файла `.env`
(`app/config.py`, класс `Settings`).

| Переменная                   | Значение по умолчанию          | Описание                                            |
| ---------------------------- | ------------------------------ | --------------------------------------------------- |
| `DATABASE_URL`               | `sqlite:///./sqlite.db`        | DSN базы данных                                     |
| `SECRET_KEY`                 | `change-me-in-production`      | Ключ подписи JWT                                    |
| `ALGORITHM`                  | `HS256`                        | Алгоритм подписи JWT                                |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `60`                           | Время жизни access-токена                           |
| `LOG_LEVEL`                  | `INFO`                         | Уровень логирования (`DEBUG`/`INFO`/`WARNING`/...)  |
| `APP_HOST`                   | `0.0.0.0`                      | Адрес HTTP-сервера                                  |
| `APP_PORT`                   | `8000`                         | Порт HTTP-сервера                                   |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | `blog` / `blog` / `blog` | Креды контейнера Postgres в `docker-compose.yml` |

Шаблон файла окружения — `.env.example`. Скопируйте его в `.env`
и при необходимости подкорректируйте значения.

## Запуск через Docker (рекомендуется)

```bash
cp .env.example .env   # если .env ещё не создан
docker compose up --build
```

Что произойдёт:

1. Поднимется контейнер `db` (PostgreSQL 16) с healthcheck.
2. Контейнер `app` дождётся готовности БД, выполнит `alembic upgrade head`
   (миграции применяются автоматически из `entrypoint.sh`) и запустит uvicorn.
3. API будет доступен на [http://localhost:8000](http://localhost:8000).
   Документация — [http://localhost:8000/docs](http://localhost:8000/docs).

Логи приложения смотреть так:

```bash
docker compose logs -f app
```

Остановить и удалить контейнеры (данные Postgres остаются в томе
`postgres_data`):

```bash
docker compose down
```

## Локальный запуск (без Docker)

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# или: venv\Scripts\activate.bat (cmd) / venv\Scripts\Activate.ps1 (PowerShell)

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

По умолчанию используется SQLite (`sqlite:///./sqlite.db`).

## Миграции

Новую миграцию можно сгенерировать после изменения моделей:

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

В контейнере `alembic upgrade head` запускается автоматически на старте.

## Логирование

`app/logging_config.py` настраивает корневой логгер по `LOG_LEVEL`.
HTTP-middleware в `app/main.py` пишет на каждый запрос строку вида:

```
2026-05-17 21:15:42 [INFO] app.access: POST /posts -> 200 [user_id=7] 12.34ms
```

Если запрос анонимный — будет `[anonymous]`, при некорректном JWT —
`[invalid_token]`. Логи приложения и uvicorn идут в stdout, чтобы их
собирал `docker logs` / `docker compose logs`.
