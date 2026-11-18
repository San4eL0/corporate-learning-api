import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_swagger(client):
    res = client.get("/openapi.json")
    assert res.status_code == 200
    assert "/students" in str(res.json()["paths"])


def test_crud_cycle(client):
    created = client.post(
        "/students",
        json={
            "full_name": "Иван Петров",
            "email": "ivan@example.com",
        },
    )
    assert created.status_code == 201
    student_id = created.json()["id"]

    got = client.get(f"/students/{student_id}")
    assert got.status_code == 200
    assert got.json()["email"] == "ivan@example.com"

    updated = client.put(
        f"/students/{student_id}",
        json={"full_name": "Иван Иванов"},
    )
    assert updated.status_code == 200
    assert updated.json()["full_name"] == "Иван Иванов"

    deleted = client.delete(f"/students/{student_id}")
    assert deleted.status_code == 200

    missing = client.get(f"/students/{student_id}")
    assert missing.status_code == 404


def test_validation_rejects_bad_email(client):
    res = client.post(
        "/employees",
        json={
            "full_name": "Мария",
            "email": "not-an-email",
        },
    )
    assert res.status_code == 400


def test_employee_crud(client):
    created = client.post(
        "/employees",
        json={
            "full_name": "Пётр Сидоров",
            "email": "petr@corp.com",
            "department": "Разработка",
        },
    )
    assert created.status_code == 201
    assert created.json()["department"] == "Разработка"


def test_schedule_in_progress(client):
    from datetime import datetime, timedelta

    emp = client.post(
        "/employees",
        json={"full_name": "Аня", "email": "anya@corp.com"},
    ).json()
    course = client.post(
        "/courses",
        json={"title": "FastAPI", "duration_hours": 10},
    ).json()

    now = datetime.utcnow()
    created = client.post(
        "/schedule",
        json={
            "employee_id": emp["id"],
            "course_id": course["id"],
            "starts_at": (now - timedelta(hours=1)).isoformat(),
            "ends_at": (now + timedelta(hours=1)).isoformat(),
        },
    )
    assert created.status_code == 201

    res = client.get("/schedule/in-progress")
    assert res.status_code == 200
    assert any(item["id"] == created.json()["id"] for item in res.json())


def test_schedule_rejects_overlap(client):
    from datetime import datetime, timedelta

    emp = client.post(
        "/employees",
        json={"full_name": "Боря", "email": "borya@corp.com"},
    ).json()
    course = client.post(
        "/courses",
        json={"title": "Python", "duration_hours": 5},
    ).json()

    now = datetime.utcnow()
    body = {
        "employee_id": emp["id"],
        "course_id": course["id"],
        "starts_at": (now - timedelta(hours=1)).isoformat(),
        "ends_at": (now + timedelta(hours=1)).isoformat(),
    }
    first = client.post("/schedule", json=body)
    assert first.status_code == 201

    overlap = client.post(
        "/schedule",
        json={
            **body,
            "starts_at": now.isoformat(),
            "ends_at": (now + timedelta(minutes=30)).isoformat(),
        },
    )
    assert overlap.status_code == 400