from flask import Flask,request, jsonify

from src.models import Teacher,DictData,init_dict_data,db,app
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

# === 初始化数据库 ===
with app.app_context():
    db.create_all()
    init_dict_data()

# to run the application: python main.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)