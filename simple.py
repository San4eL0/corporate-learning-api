"""
Практическая работа №8 — вариант 28 (корпоративное обучение).
Упрощённая версия: один файл, запуск одной командой:  python3 simple.py
Swagger / документация:  http://127.0.0.1:8000/docs
"""
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship

# ---------- БД ----------
engine = create_engine("sqlite:///learning_simple.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ---------- Сущности ----------
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration_hours = Column(Integer, default=0)


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)


Base.metadata.create_all(engine)


# ---------- Схемы (валидация) ----------
class EmployeeIn(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    department: str | None = None

    class Config:
        from_attributes = True


class CourseIn(BaseModel):
    title: str
    duration_hours: int = 0


class CourseOut(BaseModel):
    id: int
    title: str
    duration_hours: int

    class Config:
        from_attributes = True


class ScheduleIn(BaseModel):
    employee_id: int
    course_id: int
    starts_at: datetime
    ends_at: datetime


# ---------- Приложение ----------
app = FastAPI(title="Практика №8 (вариант 28) — просто", version="1.0.0")


def db():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


def get_db():
    return Depends(db)


# --- CRUD Employee ---
@app.get("/employees", response_model=list[EmployeeOut])
def list_employees(d: Session = Depends(db)):
    return d.query(Employee).all()


@app.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(body: EmployeeIn, d: Session = Depends(db)):
    if d.query(Employee).filter_by(email=body.email).first():
        raise HTTPException(400, "email уже занят")
    emp = Employee(name=body.name, email=body.email, department=body.department)
    d.add(emp)
    d.commit()
    return emp


# --- CRUD Course ---
@app.get("/courses", response_model=list[CourseOut])
def list_courses(d: Session = Depends(db)):
    return d.query(Course).all()


@app.post("/courses", response_model=CourseOut, status_code=201)
def create_course(body: CourseIn, d: Session = Depends(db)):
    c = Course(title=body.title, duration_hours=body.duration_hours)
    d.add(c)
    d.commit()
    return c


# --- CRUD Schedule ---
@app.post("/schedule", status_code=201)
def create_schedule(body: ScheduleIn, d: Session = Depends(db)):
    if body.ends_at <= body.starts_at:
        raise HTTPException(400, "ends_at должна быть позже starts_at")
    clash = d.query(Schedule).filter(
        Schedule.employee_id == body.employee_id,
        Schedule.starts_at < body.ends_at,
        Schedule.ends_at > body.starts_at,
    ).first()
    if clash:
        raise HTTPException(400, "у сотрудника уже есть занятие в этом времени")
    s = Schedule(**body.model_dump())
    d.add(s)
    d.commit()
    return s


# ---------- Специфический GET варианта: обучение прямо сейчас ----------
@app.get("/schedule/in-progress")
def in_progress(d: Session = Depends(db)):
    now = datetime.utcnow()
    rows = d.query(Schedule).filter(
        Schedule.starts_at <= now, Schedule.ends_at >= now
    ).all()
    out = []
    for r in rows:
        emp = d.query(Employee).get(r.employee_id)
        course = d.query(Course).get(r.course_id)
        out.append({
            "employee": emp.name if emp else r.employee_id,
            "course": course.title if course else r.course_id,
            "starts_at": r.starts_at,
            "ends_at": r.ends_at,
        })
    return out


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)