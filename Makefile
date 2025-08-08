# Создадим Makefile в корне проекта
makefile_path = os.path.join(extract_path, "project-root", "Makefile")

makefile_content = """
# Makefile for managing backend

.PHONY: install run migrate makemigrations test docker-build docker-up

install:
\tcd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

run:
\tcd backend && source venv/bin/activate && uvicorn app.main:app --reload

makemigrations:
\tcd backend && alembic revision --autogenerate -m "Auto migration"

migrate:
\tcd backend && alembic upgrade head

test:
\tcd backend && pytest

docker-build:
\tdocker build -t assembly-backend ./backend

docker-up:
\tdocker-compose up --build
"""

with open(makefile_path, "w", encoding="utf-8") as f:
    f.write(makefile_content.strip())

# Проверим, что Makefile создан
os.path.exists(makefile_path)
