# FastAPI + Django SQLite

Проект подключается к существующей SQLite базе данных Django и использует репозитории для работы с сущностями.

## Сущности
- Category
- Location
- Post
- Comment

## Запуск

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```