from datetime import datetime, time
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.services import ScheduleService

from app.models import Schedule


def _payload(employee_id=1, course_id=1, start=None, end=None):
    return MagicMock(
        model_dump=lambda: {
            "employee_id": employee_id,
            "course_id": course_id,
            "starts_at": start,
            "ends_at": end,
            "created_at": datetime.utcnow(),
        }
    )


class TestScheduleValidation:
    def test_rejects_ends_before_start(self):
        start = datetime(2026, 1, 10, 10, 0)
        end = datetime(2026, 1, 10, 9, 0)
        repo = MagicMock()
        service = ScheduleService(MagicMock(db=repo))
        service.repo = repo
        repo.overlaps.return_value = None
        with pytest.raises(HTTPException) as exc:
            service.create(_payload(start=start, end=end))
        assert exc.value.status_code == 400

    def test_rejects_overlapping_schedule(self):
        start = datetime(2026, 1, 10, 10, 0)
        end = datetime(2026, 1, 10, 12, 0)
        repo = MagicMock()
        repo.overlaps.return_value = Schedule(id=1)
        service = ScheduleService(MagicMock(db=repo))
        service.repo = repo
        with pytest.raises(HTTPException) as exc:
            service.create(_payload(start=start, end=end))
        assert exc.value.status_code == 400

    def test_creates_valid_schedule(self):
        start = datetime(2026, 1, 10, 10, 0)
        end = datetime(2026, 1, 10, 12, 0)
        repo = MagicMock()
        repo.overlaps.return_value = None
        repo.create.return_value = Schedule(id=1)
        service = ScheduleService(MagicMock(db=repo))
        service.repo = repo
        result = service.create(_payload(start=start, end=end))
        assert result.id == 1