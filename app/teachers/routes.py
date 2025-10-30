from flask import render_template, redirect, url_for, flash, request
from . import teachers
from ..models import Teacher, DictData, db
from flask_login import login_required
from datetime import datetime

@teachers.route('/list')
@login_required
def teacher_list():
    teachers = Teacher.query.all()
    return render_template('teachers/list.html', teachers=teachers)

@teachers.route('/add', methods=['GET', 'POST'])
@login_required
def teacher_add():
    majors = DictData.query.filter_by(topic='专业').all()
    educations = DictData.query.filter_by(topic='学历').all()
    degrees = DictData.query.filter_by(topic='学位').all()
    positions = DictData.query.filter_by(topic='职务').all()
    
    if request.method == 'POST':
        try:
            # 创建新教师
            teacher = Teacher(
                name=request.form['name'],
                gender=request.form['gender'],
                birth_date=datetime.strptime(request.form['birth_date'], '%Y-%m-%d') if request.form['birth_date'] else None,
                employee_id=request.form['employee_id'],
                phone=request.form['phone'],
                email=request.form['email'],
                hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d') if request.form['hire_date'] else None,
                department=request.form['department'],
                major_id=request.form['major_id'] if request.form['major_id'] else None,
                education_id=request.form['education_id'] if request.form['education_id'] else None,
                degree_id=request.form['degree_id'] if request.form['degree_id'] else None,
                position_id=request.form['position_id'] if request.form['position_id'] else None,
                has_teaching_certificate='has_teaching_certificate' in request.form,
                has_industry_experience='has_industry_experience' in request.form,
                research_direction=request.form['research_direction'],
                introduction=request.form['introduction']
            )
            db.session.add(teacher)
            db.session.commit()
            flash('教师信息添加成功！')
            return redirect(url_for('teachers.teacher_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}')
    
    return render_template('teachers/add.html', 
                          majors=majors, 
                          educations=educations,
                          degrees=degrees,
                          positions=positions)

@teachers.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def teacher_edit(id):
    teacher = Teacher.query.get_or_404(id)
    majors = DictData.query.filter_by(topic='专业').all()
    educations = DictData.query.filter_by(topic='学历').all()
    degrees = DictData.query.filter_by(topic='学位').all()
    positions = DictData.query.filter_by(topic='职务').all()
    
    if request.method == 'POST':
        try:
            teacher.name = request.form['name']
            teacher.gender = request.form['gender']
            teacher.birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d') if request.form['birth_date'] else None
            teacher.employee_id = request.form['employee_id']
            teacher.phone = request.form['phone']
            teacher.email = request.form['email']
            teacher.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d') if request.form['hire_date'] else None
            teacher.department = request.form['department']
            teacher.major_id = request.form['major_id'] if request.form['major_id'] else None
            teacher.education_id = request.form['education_id'] if request.form['education_id'] else None
            teacher.degree_id = request.form['degree_id'] if request.form['degree_id'] else None
            teacher.position_id = request.form['position_id'] if request.form['position_id'] else None
            teacher.has_teaching_certificate = 'has_teaching_certificate' in request.form
            teacher.has_industry_experience = 'has_industry_experience' in request.form
            teacher.research_direction = request.form['research_direction']
            teacher.introduction = request.form['introduction']
            
            db.session.commit()
            flash('教师信息更新成功！')
            return redirect(url_for('teachers.teacher_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}')
    
    return render_template('teachers/edit.html', 
                          teacher=teacher,
                          majors=majors,
                          educations=educations,
                          degrees=degrees,
                          positions=positions)

@teachers.route('/delete/<int:id>')
@login_required
def teacher_delete(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        flash('教师信息删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}')
    return redirect(url_for('teachers.teacher_list'))

@teachers.route('/detail/<int:id>')
def teacher_detail(id):
    teacher = Teacher.query.get_or_404(id)
    return render_template('teachers/detail.html', teacher=teacher)