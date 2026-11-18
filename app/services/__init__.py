from typing import Optional

from fastapi import HTTPException

from app.repositories import (
    CourseRepository,
    EmployeeRepository,
    ScheduleRepository,
    StudentGroupRepository,
    StudentRepository,
    SubjectRepository,
    TeacherRepository,
)


class EntityService:
    repo_cls = None
    entity_name = "entity"

    def __init__(self, db):
        self.repo = self.repo_cls(db)

    def _not_found(self):
        raise HTTPException(status_code=404, detail=f"{self.entity_name} not found")

    def list(self):
        return self.repo.all()

    def get(self, obj_id: int):
        obj = self.repo.get(obj_id)
        if not obj:
            self._not_found()
        return obj

    def create(self, payload):
        return self.repo.create(payload.model_dump(exclude_unset=True))

    def update(self, obj_id: int, payload):
        obj = self.repo.get(obj_id)
        if not obj:
            self._not_found()
        return self.repo.update(obj, payload.model_dump(exclude_unset=True))

    def delete(self, obj_id: int):
        obj = self.repo.get(obj_id)
        if not obj:
            self._not_found()
        self.repo.delete(obj)
        return {"detail": "deleted"}


class StudentGroupService(EntityService):
    repo_cls = StudentGroupRepository
    entity_name = "StudentGroup"


class CourseService(EntityService):
    repo_cls = CourseRepository
    entity_name = "Course"


class SubjectService(EntityService):
    repo_cls = SubjectRepository
    entity_name = "Subject"


class TeacherService(EntityService):
    repo_cls = TeacherRepository
    entity_name = "Teacher"


class StudentService(EntityService):
    repo_cls = StudentRepository
    entity_name = "Student"


class EmployeeService(EntityService):
    repo_cls = EmployeeRepository
    entity_name = "Employee"


class ScheduleService(EntityService):
    repo_cls = ScheduleRepository
    entity_name = "Schedule"

    def create(self, payload):
        data = payload.model_dump()
        if data["ends_at"] <= data["starts_at"]:
            raise HTTPException(
                status_code=400, detail="ends_at must be after starts_at"
            )
        if self.repo.overlaps(data["employee_id"], data["starts_at"], data["ends_at"]):
            raise HTTPException(
                status_code=400,
                detail="employee already has a schedule in this time range",
            )
        return self.repo.create(data)

    def update(self, obj_id: int, payload):
        obj = self.repo.get(obj_id)
        if not obj:
            self._not_found()
        data = payload.model_dump(exclude_unset=True)
        starts = data.get("starts_at", obj.starts_at)
        ends = data.get("ends_at", obj.ends_at)
        employee_id = data.get("employee_id", obj.employee_id)
        if ends <= starts:
            raise HTTPException(
                status_code=400, detail="ends_at must be after starts_at"
            )
        if self.repo.overlaps(employee_id, starts, ends):
            raise HTTPException(
                status_code=400,
                detail="employee already has a schedule in this time range",
            )
        return self.repo.update(obj, data)

    def in_progress(self):
        return self.repo.actives_in_progress()