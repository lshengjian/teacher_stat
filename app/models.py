from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

# 字典数据模型
class DictData(db.Model):
    __tablename__ = 'dict_data'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100))
    name = db.Column(db.String(100))  # 添加name字段
    sort = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {'id': self.id, 'topic': self.topic, 'name': self.name, 'sort': self.sort, 'level': self.level}
    
# === 初始化字典数据 ===
def init_dict_data():
    dicts = [
        {'topic': '专业', 'name': '数字媒体技术', 'sort': 1},
        {'topic': '专业', 'name': '动画', 'sort': 2},
        {'topic': '专业', 'name': '网络与新媒体', 'sort': 3},

        {'topic': '学历', 'name': '本科', 'sort': 1},
        {'topic': '学历', 'name': '硕士研究生', 'sort': 2},
        {'topic': '学历', 'name': '博士研究生', 'sort': 3},

        {'topic': '学位', 'name': '学士', 'sort': 1},
        {'topic': '学位', 'name': '硕士', 'sort': 2},
        {'topic': '学位', 'name': '工程硕士', 'sort': 3},
        {'topic': '学位', 'name': '博士', 'sort': 4},   

        {'topic': '职务', 'name': '教授', 'sort': 1, 'level': 1},
        {'topic': '职务', 'name': '副教授', 'sort': 2, 'level': 1},
        {'topic': '职务', 'name': '其他高级', 'sort': 3, 'level': 1},
        {'topic': '职务', 'name': '讲师', 'sort': 4, 'level': 2},
        {'topic': '职务', 'name': '其他中级', 'sort': 5, 'level': 2},
        {'topic': '职务', 'name': '助教', 'sort': 6, 'level': 3},
        {'topic': '职务', 'name': '无', 'sort': 7, 'level': 4},
        
        {'topic': '项目级别', 'name': '国家级', 'sort': 1},
        {'topic': '项目级别', 'name': '省部级', 'sort': 2},
        {'topic': '项目级别', 'name': '校级', 'sort': 3},
        {'topic': '项目级别', 'name': '横向', 'sort': 4},
        
        {'topic': '论文级别', 'name': 'SCI', 'sort': 1},
        {'topic': '论文级别', 'name': 'EI', 'sort': 2},
        {'topic': '论文级别', 'name': '中文核心', 'sort': 3},
        {'topic': '论文级别', 'name': '普通期刊', 'sort': 4},
    ]
    for d in dicts:
        if not DictData.query.filter_by(topic=d['topic'], name=d['name']).first():
            db.session.add(DictData(**d))
    db.session.commit()
# 教师基本信息模型
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    department = db.Column(db.String(100))
    major_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 专业
    education_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 学历
    degree_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 学位
    position_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 职务
    has_teaching_certificate = db.Column(db.Boolean, default=False)  # 是否具有教师资格证
    has_industry_experience = db.Column(db.Boolean, default=False)  # 是否具有行业经验
    research_direction = db.Column(db.String(200))
    introduction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    projects = db.relationship('Project', backref='teacher', lazy=True)
    papers = db.relationship('Paper', backref='teacher', lazy=True)
    
    # 字典数据关系
    major = db.relationship('DictData', foreign_keys=[major_id])
    education = db.relationship('DictData', foreign_keys=[education_id])
    degree = db.relationship('DictData', foreign_keys=[degree_id])
    position = db.relationship('DictData', foreign_keys=[position_id])
    
    def __repr__(self):
        return f'<Teacher {self.name}>'

# 项目信息模型
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    project_no = db.Column(db.String(50))
    project_level_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 项目级别
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    funding = db.Column(db.Float)  # 经费
    role = db.Column(db.String(50))  # 角色
    status = db.Column(db.String(20))  # 状态
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    project_level = db.relationship('DictData')
    
    def __repr__(self):
        return f'<Project {self.name}>'

# 论文信息模型
class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    journal = db.Column(db.String(200))
    paper_level_id = db.Column(db.Integer, db.ForeignKey('dict_data.id'))  # 论文级别
    publish_date = db.Column(db.Date)
    author_order = db.Column(db.Integer)  # 作者排序
    is_corresponding = db.Column(db.Boolean, default=False)  # 是否通讯作者
    doi = db.Column(db.String(100))
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(200))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    paper_level = db.relationship('DictData')
    
    def __repr__(self):
        return f'<Paper {self.title}>'
