from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentGroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None


class StudentGroupCreate(StudentGroupBase):
    pass


class StudentGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None


class StudentGroupOut(StudentGroupBase):
    id: int

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    duration_hours: int = Field(0, ge=0)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    duration_hours: Optional[int] = Field(None, ge=0)


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True


class SubjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    course_id: Optional[int] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    course_id: Optional[int] = None


class SubjectOut(SubjectBase):
    id: int

    class Config:
        from_attributes = True


class TeacherBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    specialization: Optional[str] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None


class TeacherOut(BaseModel):
    id: int
    full_name: str
    email: str
    specialization: Optional[str] = None

    class Config:
        from_attributes = True


class StudentBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    group_id: Optional[int] = None
    enrolled_at: Optional[date] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    group_id: Optional[int] = None
    enrolled_at: Optional[date] = None


class StudentOut(BaseModel):
    id: int
    full_name: str
    email: str
    group_id: Optional[int] = None
    enrolled_at: Optional[date] = None

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    department: Optional[str] = None
    hired_at: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    hired_at: Optional[date] = None


class EmployeeOut(BaseModel):
    id: int
    full_name: str
    email: str
    department: Optional[str] = None
    hired_at: Optional[date] = None

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    employee_id: int
    course_id: int
    starts_at: datetime
    ends_at: datetime


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    employee_id: Optional[int] = None
    course_id: Optional[int] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None


class ScheduleOut(BaseModel):
    id: int
    employee_id: int
    course_id: int
    starts_at: datetime
    ends_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True