from flask import request, jsonify, send_file
from datetime import date
import pandas as pd
from io import BytesIO
from src.models import Teacher,db
from src.utils import get_age_title_stat,load_define


def get_teachers():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # 获取过滤参数
    filters = request.args.to_dict()
    
    # 构建查询
    query = Teacher.query
    
    if filters.get('major'):
        query = query.filter(Teacher.major == filters['major'])
    if filters.get('title'):
        query = query.filter(Teacher.title == filters['title'])
    if filters.get('degree'):
        query = query.filter(Teacher.highest_degree == filters['degree'])
    
    # 执行分页查询
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    teachers = [t.to_dict() for t in pagination.items]
    
    # 返回分页结果
    return jsonify({
        'teachers': teachers,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page
    })

def create_teacher():
    data = request.json
    
    if 'birth_date' in data and data['birth_date']:
        data['birth_date'] = date.fromisoformat(data['birth_date'])
    if 'hire_date' in data and data['hire_date']:
        data['hire_date'] = date.fromisoformat(data['hire_date'])
    teacher = Teacher(**data)
    print(data)
    print(teacher.to_dict())

    db.session.add(teacher)
    db.session.commit()
    return jsonify(teacher.to_dict()), 201

def update_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.json
    print(data)
    # 获取字典数据
    
    # 排除计算属性和关系属性
    excluded_keys = ['age', 'years_in_school']
    
    # 处理日期字段
    date_fields = ['birth_date', 'hire_date']
    for field in date_fields:
        if field in data and data[field]:
            data[field] = date.fromisoformat(data[field])
    
    # 检查工号唯一性
    if 'employee_id' in data and data['employee_id'] != teacher.employee_id:
        existing_teacher = Teacher.query.filter_by(employee_id=data['employee_id']).first()
        if existing_teacher:
            return jsonify({'error': '工号已存在'}), 400
    
    # 更新教师信息
    for key, value in data.items():
        if key not in excluded_keys:
            setattr(teacher, key, value)
    
    try:
        db.session.commit()
        return jsonify(teacher.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败: ' + str(e)}), 400


def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        return '', 204  # 返回204状态码表示删除成功且无内容返回
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败: ' + str(e)}), 400

def export_teachers():
    filters = request.args.to_dict()
    query = Teacher.query
    if filters.get('major'):
        query = query.filter(Teacher.major == filters['major'])
    if filters.get('title'):
        query = query.filter(Teacher.title == filters['title'])
    if filters.get('degree'):
        query = query.filter(Teacher.highest_degree == filters['degree'])
    teachers = [t.to_dict() for t in query.all()]

    df = pd.DataFrame(teachers)
    dfs=load_define('teacher')
    col_map={}
    for f in dfs:
        name=f.get('name_en','').strip()
        if name.startswith('@'):
            name=name[1:]
        col_map[name]=f.get('name_zh','')

  
    df = df.rename(columns=col_map)
    
    bool_cols = df.select_dtypes(include='bool').columns
    df[bool_cols] = df[bool_cols].replace({True: '是', False: '否'})

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='教师信息')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='teachers.xlsx'
    )

def export_stat_teachers(teachers, cut_points=[30, 40, 60]):
    stat = get_age_title_stat(teachers, cut_points)
    
    # 准备数据用于导出
    data = []
    # 表头
    headers = ['职称']
    headers.extend(stat['age_groups'])
    
    # 数据行
    for i, title in enumerate(stat['titles']):
        row = [title]
        row.extend(stat['data'][i])
        data.append(row)
    
    df = pd.DataFrame(data, columns=headers)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='职称-年龄段统计')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='stat_teachers.xlsx'
    )