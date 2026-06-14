# FastAPI Blog

Финальный проект курса: REST API блога на FastAPI. Всё асинхронно, в Docker
поднимается PostgreSQL, локально можно работать через SQLite. Есть JWT,
Alembic, логирование запросов, refresh-токены и несколько картинок к посту.

## Быстрый старт

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

Миграции накатываются сами при старте контейнера.

Логи:

```bash
docker compose logs -f app
```

Остановить:

```bash
docker compose down
```

## Локально без Docker

Нужен Python 3.12.

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Заметки

- Настройки — в `.env.example` (`DATABASE_URL`, `SECRET_KEY`, `UPLOAD_DIR` и др.).
- Auth: `login`/`register` отдают `access_token` + `refresh_token`.
  Обновление: `POST /auth/refresh` с телом `{"refresh_token": "..."}`.
  Выход: `POST /auth/logout` с тем же телом.
- Картинки к посту: `POST /posts/{id}/image` или `/images` (до 10 штук).
  Список в поле `images`, удаление: `DELETE /posts/{id}/images/{image_id}`.
- Новая миграция: `alembic revision --autogenerate -m "..."`, затем `alembic upgrade head`.
