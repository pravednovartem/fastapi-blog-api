#!/bin/sh
set -e

python <<'PYEOF'
import os
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from app.config import to_sync_database_url

url = to_sync_database_url(
    os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./sqlite.db"),
)
if url.startswith("sqlite"):
    sys.exit(0)

attempts = 30
engine = create_engine(url, pool_pre_ping=True)
for i in range(1, attempts + 1):
    try:
        with engine.connect():
            print(f"[entrypoint] database is ready (attempt {i})")
            sys.exit(0)
    except OperationalError as exc:
        print(f"[entrypoint] database not ready ({i}/{attempts}): {exc}")
        time.sleep(2)

print("[entrypoint] database is not reachable, exiting", file=sys.stderr)
sys.exit(1)
PYEOF

echo "[entrypoint] applying alembic migrations"
alembic upgrade head

echo "[entrypoint] starting: $*"
exec "$@"
