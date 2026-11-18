# Corporate Learning REST API

Практическая работа №8 — «Разработка кода информационных ресурсов»
**Вариант 28 (Блок Е — корпоративное обучение)**.

REST API на **Python + FastAPI** с CRUD, валидацией, бизнес-логикой и Swagger-документацией.

## Технологии

- Python 3.11 + FastAPI
- SQLAlchemy 2 (ORM), SQLite (БД)
- Pydantic v2 (валидация)
- Swagger / OpenAPI (авто-документация)
- pytest (unit-тесты)

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте http://127.0.0.1:8000/docs — интерактивный Swagger со всеми эндпоинтами.

## Тесты

```bash
pytest -q
```

## Структура проекта (слои)

```
app/
  main.py            # приложение, глобальные обработчики ошибок (404, 500, 400)
  database.py        # подключение и сессия БД
  models/            # SQLAlchemy-модели (сущности)
  schemas/           # Pydantic-схемы (валидация входных данных)
  repositories/      # слой доступа к данным
  services/          # бизнес-логика
  routers/           # Controller-слой (эндпоинты)
tests/               # unit-тесты
```

## Сущности

- `Student`, `StudentGroup`, `Course`, `Subject`, `Teacher` — базовые
- `Employee` — дополнительная сущность варианта (сотрудник компании)
- `Schedule` — расписание обучения (сотрудник ↔ курс)

## CRUD

Для всех сущностей: `GET /`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`.

## Специфика варианта 28

- **Доп. сущность** — `Employee` (сотрудник).
- **Специфический GET** — `GET /schedule/in-progress` — обучение, идущее прямо сейчас.
- **Бизнес-правило** — у сотрудника не может быть двух расписаний в пересекающийся промежуток времени (400 Bad Request).