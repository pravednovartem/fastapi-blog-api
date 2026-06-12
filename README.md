# FastAPI Blog

Финальный проект курса: REST API блога на FastAPI. Всё асинхронно, в Docker
поднимается PostgreSQL, локально можно работать через SQLite. Есть JWT,
Alembic, логирование запросов и загрузка одной картинки к посту.

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
- Картинка к посту: сначала `POST /posts`, потом `POST /posts/{id}/image`
  (поле `image`, jpg/png/gif/webp, до 5 MB). URL будет в поле `image` поста.
- Новая миграция: `alembic revision --autogenerate -m "..."`, затем `alembic upgrade head`.
