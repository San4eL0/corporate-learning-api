from datetime import datetime, time, timezone

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models import (
    Course,
    Employee,
    Schedule,
    Student,
    StudentGroup,
    Subject,
    Teacher,
)


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _all(self, model):
        return self.db.query(model).all()

    def _get(self, model, obj_id: int):
        return self.db.query(model).filter(model.id == obj_id).first()

    def _save(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def _delete(self, obj):
        self.db.delete(obj)
        self.db.commit()


class StudentGroupRepository(BaseRepository):
    def all(self):
        return self._all(StudentGroup)

    def get(self, obj_id):
        return self._get(StudentGroup, obj_id)

    def create(self, data):
        return self._save(StudentGroup(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class CourseRepository(BaseRepository):
    def all(self):
        return self._all(Course)

    def get(self, obj_id):
        return self._get(Course, obj_id)

    def create(self, data):
        return self._save(Course(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class SubjectRepository(BaseRepository):
    def all(self):
        return self._all(Subject)

    def get(self, obj_id):
        return self._get(Subject, obj_id)

    def create(self, data):
        return self._save(Subject(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class TeacherRepository(BaseRepository):
    def all(self):
        return self._all(Teacher)

    def get(self, obj_id):
        return self._get(Teacher, obj_id)

    def create(self, data):
        return self._save(Teacher(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class StudentRepository(BaseRepository):
    def all(self):
        return self._all(Student)

    def get(self, obj_id):
        return self._get(Student, obj_id)

    def create(self, data):
        return self._save(Student(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class EmployeeRepository(BaseRepository):
    def all(self):
        return self._all(Employee)

    def get(self, obj_id):
        return self._get(Employee, obj_id)

    def create(self, data):
        return self._save(Employee(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)


class ScheduleRepository(BaseRepository):
    def all(self):
        return self._all(Schedule)

    def get(self, obj_id):
        return self._get(Schedule, obj_id)

    def create(self, data):
        return self._save(Schedule(**data))

    def update(self, obj, data):
        for k, v in data.items():
            setattr(obj, k, v)
        return self._save(obj)

    def delete(self, obj):
        self._delete(obj)

    def actives_in_progress(self):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return (
            self.db.query(Schedule)
            .filter(
                and_(
                    Schedule.starts_at <= now,
                    Schedule.ends_at >= now,
                )
            )
            .all()
        )

    def overlaps(self, employee_id: int, starts_at, ends_at):
        return (
            self.db.query(Schedule)
            .filter(
                Schedule.employee_id == employee_id,
                Schedule.starts_at < ends_at,
                Schedule.ends_at > starts_at,
            )
            .first()
        )