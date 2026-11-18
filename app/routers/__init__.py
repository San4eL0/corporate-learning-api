from app.routers.factory import crud_router
from app.routers.schedule import router as schedule_router
from app.schemas import (
    CourseCreate,
    CourseOut,
    CourseUpdate,
    EmployeeCreate,
    EmployeeOut,
    EmployeeUpdate,
    StudentCreate,
    StudentGroupCreate,
    StudentGroupOut,
    StudentGroupUpdate,
    StudentOut,
    StudentUpdate,
    SubjectCreate,
    SubjectOut,
    SubjectUpdate,
    TeacherCreate,
    TeacherOut,
    TeacherUpdate,
)
from app.services import (
    CourseService,
    EmployeeService,
    StudentGroupService,
    StudentService,
    SubjectService,
    TeacherService,
)

student_group_router = crud_router(
    prefix="/groups",
    tags=["student-groups"],
    service_cls=StudentGroupService,
    create_schema=StudentGroupCreate,
    update_schema=StudentGroupUpdate,
    out_schema=StudentGroupOut,
)

course_router = crud_router(
    prefix="/courses",
    tags=["courses"],
    service_cls=CourseService,
    create_schema=CourseCreate,
    update_schema=CourseUpdate,
    out_schema=CourseOut,
)

subject_router = crud_router(
    prefix="/subjects",
    tags=["subjects"],
    service_cls=SubjectService,
    create_schema=SubjectCreate,
    update_schema=SubjectUpdate,
    out_schema=SubjectOut,
)

teacher_router = crud_router(
    prefix="/teachers",
    tags=["teachers"],
    service_cls=TeacherService,
    create_schema=TeacherCreate,
    update_schema=TeacherUpdate,
    out_schema=TeacherOut,
)

student_router = crud_router(
    prefix="/students",
    tags=["students"],
    service_cls=StudentService,
    create_schema=StudentCreate,
    update_schema=StudentUpdate,
    out_schema=StudentOut,
)

employee_router = crud_router(
    prefix="/employees",
    tags=["employees"],
    service_cls=EmployeeService,
    create_schema=EmployeeCreate,
    update_schema=EmployeeUpdate,
    out_schema=EmployeeOut,
)

ALL_ROUTERS = [
    student_group_router,
    course_router,
    subject_router,
    teacher_router,
    student_router,
    employee_router,
    schedule_router,
]

__all__ = ["ALL_ROUTERS"]