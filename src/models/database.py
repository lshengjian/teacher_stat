# my_app/models.py
from flask_sqlalchemy import SQLAlchemy

# 1. 创建一个未绑定到任何 app 的 SQLAlchemy 实例
db = SQLAlchemy()

class DictData(db.Model):
    __tablename__ = 'dict_data'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    sort = db.Column(db.Integer)

    def to_dict(self):
        return {'type': self.type, 'name': self.name}
    
# === 初始化字典数据 ===
def init_dict_data():
    dicts = [
        {'type': 'major',  'name': '数字媒体技术', 'sort': 1},
        {'type': 'major', 'name': '动画', 'sort': 2},
        {'type': 'major', 'name': '网络与新媒体', 'sort': 3},

        {'type': 'education', 'name': '本科', 'sort': 1},
        {'type': 'education', 'name': '硕士研究生', 'sort': 2},
        {'type': 'education', 'name': '博士研究生', 'sort': 3},

        {'type': 'degree', 'name': '学士', 'sort': 1},
        {'type': 'degree', 'name': '硕士', 'sort': 2},
        {'type': 'degree', 'name': '工程硕士', 'sort': 3},
        {'type': 'degree', 'name': '博士', 'sort': 4},

        {'type': 'title', 'name': '教授', 'sort': 1},
        {'type': 'title', 'name': '副教授', 'sort': 2},
        {'type': 'title', 'name': '其他高级', 'sort': 3},
        {'type': 'title', 'name': '讲师', 'sort': 4},
        {'type': 'title', 'name': '其他中级', 'sort': 5},
        {'type': 'title', 'name': '助教', 'sort': 6},
        {'type': 'title', 'name': '无', 'sort': 7},
    ]
    for d in dicts:
        if not DictData.query.filter_by(type=d['type'], name=d['name']).first():
            db.session.add(DictData(**d))
    db.session.commit()
def col_from_def(d):
    
    # 支持 type 形如 "String(10)" 的写法，自动提取类型和长度
    t_raw = d.get('type', 'string')
    if '(' in t_raw and ')' in t_raw:
        t, length_str = t_raw.split('(', 1)
        t = t.strip().lower()
        length = int(length_str.rstrip(')'))
    else:
        t = t_raw.lower()
        length = None
    if t in ('string', 'varchar', 'char'):
        col_type = db.String(length or 255)
    elif t in ('text', 'textarea'):
        col_type = db.Text
    elif t in ('int', 'integer'):
        col_type = db.Integer
    elif t in ('float', 'numeric', 'decimal'):
        col_type = db.Float
    elif t in ('date',):
        col_type = db.Date
    elif t in ('datetime', 'timestamp'):
        col_type = db.DateTime
    elif t in ('bool', 'boolean'):
        col_type = db.Boolean
    else:
        col_type = db.String(length or 255)
    return db.Column(col_type, comment=d.get('name_zh', ''))