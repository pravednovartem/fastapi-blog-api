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
python -m uvicorn app.main:app --port 8001