from datetime import date
from src.utils import load_define
from src.utils import get_years
from .database import db
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    # 根据 load_define 自动生成字段，跳过以 @ 开头的计算字段
    #_defines = load_define('teacher')
    

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    major = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    highest_education = db.Column(db.String(50))
    highest_degree = db.Column(db.String(50))
    degree_major_name = db.Column(db.String(100))
    degree_institution = db.Column(db.String(100))
    title = db.Column(db.String(50))
    position = db.Column(db.String(100))
    has_teaching_cert = db.Column(db.Boolean, default=False)
    has_industry_background = db.Column(db.Boolean, default=False)
    professional_title = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    work_experience = db.Column(db.Text)
    main_courses = db.Column(db.Text)   



    @property
    def age(self):
        return get_years(self.birth_date)
    @property
    def years_in_school(self):
        return get_years(self.hire_date)

    def to_dict(self):
        d = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            # 将日期对象转换为字符串
            if isinstance(value, date):
                d[c.name] = value.isoformat()
            else:
                d[c.name] = value
        d['age'] = self.age
        d['years_in_school'] = self.years_in_school
        return d