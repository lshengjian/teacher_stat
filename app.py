# run.py
from src import create_app
from src.models import db,init_dict_data,DictData,Teacher
from flask import request, jsonify
# 创建一个应用实例
app = create_app()
from src.routes import get_teachers, create_teacher, export_teachers, update_teacher,delete_teacher,export_stat_teachers

from src.utils import  get_age_title_stat



# === 路由：首页（返回前端页面）===
@app.route('/')
def index():
    return app.send_static_file('index.html')

# === API：获取字典 ===
@app.route('/api/dict/<dict_type>')
def get_dict(dict_type):
    items = DictData.query.filter_by(type=dict_type).order_by(DictData.sort).all()
    return jsonify([item.to_dict() for item in items])

# === API：教师增删改查 ===
app.route('/api/teachers', methods=['GET'])(get_teachers)
app.route('/api/teachers', methods=['POST'])(create_teacher)
app.route('/api/teachers/<int:teacher_id>', methods=['PUT'])(update_teacher)
app.route('/api/teachers/<int:teacher_id>', methods=['DELETE'])(delete_teacher)
app.route('/api/teachers/export', methods=['GET'])(export_teachers)

@app.route('/api/stat/age-title')
def stat_age_title():
    cut_points = request.args.get('cut_points', '30,40,60')
    cut_points = [int(x) for x in cut_points.split(',')]
    teachers = Teacher.query.all()
    stat = get_age_title_stat(teachers, cut_points)
    return jsonify(stat)

@app.route('/api/stat/age-title/export')
def stat_age_title_export():
    cut_points = request.args.get('cut_points', '30,40,60')
    cut_points = [int(x) for x in cut_points.split(',')]
    teachers = Teacher.query.all()
    return export_stat_teachers(teachers, cut_points)

if __name__ == '__main__':
    # 在应用上下文中创建所有数据库表
    # 这只需要在第一次运行时执行，或者在模型更改后执行
    with app.app_context():
        
        db.create_all()
        init_dict_data()

    app.run(debug=True)