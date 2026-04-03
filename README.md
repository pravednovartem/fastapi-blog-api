# FastAPI + Django SQLite

Проект подключается к существующей SQLite базе данных Django и использует репозитории для работы с сущностями.

## Сущности
- Category
- Location
- Post
- Comment

## База данных и миграции (Alembic)

Подключение к SQLite задаётся в `app/database.py` и в `alembic.ini` (`sqlite:///./sqlite.db`).

Чтобы получить **пустую** базу с таблицами по моделям:

1. Удалите файл `sqlite.db` (если он есть).
2. Выполните `alembic upgrade head` — создастся `sqlite.db` и все таблицы из миграции `create initial tables`.

Новую миграцию после изменения моделей можно сгенерировать так:  
`alembic revision --autogenerate -m "описание изменений"`

## Первый запуск (подгрузить зависимости и поднять API)

Рекомендуется виртуальное окружение в корне проекта:

```bash
python -m venv venv
```

Активация:

- **Windows (cmd):** `venv\Scripts\activate.bat`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Git Bash / WSL:** `source venv/Scripts/activate` или `source venv/bin/activate`

Дальше из корня репозитория:

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

После старта документация API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Запуск (кратко)

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```