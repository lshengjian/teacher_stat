import include
import pytest
from datetime import date
from src.models import Teacher

class DummyDBColumn:
    def __init__(self, name, value):
        self.name = name
        self.value = value

@pytest.fixture
def teacher_instance(monkeypatch):
    # Patch __table__.columns to simulate SQLAlchemy columns
    columns = [
        DummyDBColumn('id', 1),
        DummyDBColumn('employee_id', 'T001'),
        DummyDBColumn('name', 'Alice'),
        DummyDBColumn('major', 'Math'),
        DummyDBColumn('birth_date', date(1990, 1, 1)),
        DummyDBColumn('hire_date', date(2015, 9, 1)),
    ]
    t = Teacher()
    t.id = 1
    t.employee_id = 'T001'
    t.name = 'Alice'
    t.major = 'Math'
    t.birth_date = date(1990, 1, 1)
    t.hire_date = date(2015, 9, 1)
    # Patch __table__.columns
    class DummyTable:
        pass
    DummyTable.columns = columns
    t.__table__ = DummyTable
    return t

def test_teacher_age_and_years_in_school(teacher_instance):
    assert Teacher.title.comment == '职称'
    today = date.today()
    expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))
    expected_years = today.year - 2015 - ((today.month, today.day) < (9, 1))
    assert teacher_instance.age == expected_age
    assert teacher_instance.years_in_school == expected_years

def test_teacher_to_dict(teacher_instance):
    d = teacher_instance.to_dict()
    assert d['id'] == 1
    assert d['employee_id'] == 'T001'
    assert d['name'] == 'Alice'
    assert d['major'] == 'Math'
    assert d['birth_date'] == '1990-01-01'
    assert d['hire_date'] == '2015-09-01'
    assert isinstance(d['age'], int)
    assert isinstance(d['years_in_school'], int)