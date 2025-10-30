from flask import render_template, redirect, url_for, flash, request
from . import projects
from ..models import Project, Teacher, DictData, db
from flask_login import login_required
from datetime import datetime

@projects.route('/list')
@login_required
def project_list():
    projects = Project.query.all()
    return render_template('projects/list.html', projects=projects)

@projects.route('/add', methods=['GET', 'POST'])
@login_required
def project_add():
    teachers = Teacher.query.all()
    project_levels = DictData.query.filter_by(topic='项目级别').all()
    
    if request.method == 'POST':
        try:
            # 创建新项目
            project = Project(
                name=request.form['name'],
                project_no=request.form['project_no'],
                project_level_id=request.form['project_level_id'] if request.form['project_level_id'] else None,
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d') if request.form['start_date'] else None,
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None,
                funding=float(request.form['funding']) if request.form['funding'] else 0,
                role=request.form['role'],
                status=request.form['status'],
                description=request.form['description'],
                teacher_id=request.form['teacher_id']
            )
            db.session.add(project)
            db.session.commit()
            flash('项目信息添加成功！')
            return redirect(url_for('projects.project_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}')
    
    return render_template('projects/add.html', 
                          teachers=teachers,
                          project_levels=project_levels)

@projects.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = Project.query.get_or_404(id)
    teachers = Teacher.query.all()
    project_levels = DictData.query.filter_by(topic='项目级别').all()
    
    if request.method == 'POST':
        try:
            project.name = request.form['name']
            project.project_no = request.form['project_no']
            project.project_level_id = request.form['project_level_id'] if request.form['project_level_id'] else None
            project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d') if request.form['start_date'] else None
            project.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None
            project.funding = float(request.form['funding']) if request.form['funding'] else 0
            project.role = request.form['role']
            project.status = request.form['status']
            project.description = request.form['description']
            project.teacher_id = request.form['teacher_id']
            
            db.session.commit()
            flash('项目信息更新成功！')
            return redirect(url_for('projects.project_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}')
    
    return render_template('projects/edit.html', 
                          project=project,
                          teachers=teachers,
                          project_levels=project_levels)

@projects.route('/delete/<int:id>')
@login_required
def project_delete(id):
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        flash('项目信息删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}')
    return redirect(url_for('projects.project_list'))