from flask import render_template, redirect, url_for, flash, request
from . import papers
from ..models import Paper, Teacher, DictData, db
from flask_login import login_required
from datetime import datetime

@papers.route('/list')
@login_required
def paper_list():
    papers = Paper.query.all()
    return render_template('papers/list.html', papers=papers)

@papers.route('/add', methods=['GET', 'POST'])
@login_required
def paper_add():
    teachers = Teacher.query.all()
    paper_levels = DictData.query.filter_by(topic='论文级别').all()
    
    if request.method == 'POST':
        try:
            # 创建新论文
            paper = Paper(
                title=request.form['title'],
                journal=request.form['journal'],
                paper_level_id=request.form['paper_level_id'] if request.form['paper_level_id'] else None,
                publish_date=datetime.strptime(request.form['publish_date'], '%Y-%m-%d') if request.form['publish_date'] else None,
                author_order=int(request.form['author_order']) if request.form['author_order'] else 1,
                is_corresponding='is_corresponding' in request.form,
                doi=request.form['doi'],
                abstract=request.form['abstract'],
                keywords=request.form['keywords'],
                teacher_id=request.form['teacher_id']
            )
            db.session.add(paper)
            db.session.commit()
            flash('论文信息添加成功！')
            return redirect(url_for('papers.paper_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}')
    
    return render_template('papers/add.html', 
                          teachers=teachers,
                          paper_levels=paper_levels)

@papers.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def paper_edit(id):
    paper = Paper.query.get_or_404(id)
    teachers = Teacher.query.all()
    paper_levels = DictData.query.filter_by(topic='论文级别').all()
    
    if request.method == 'POST':
        try:
            paper.title = request.form['title']
            paper.journal = request.form['journal']
            paper.paper_level_id = request.form['paper_level_id'] if request.form['paper_level_id'] else None
            paper.publish_date = datetime.strptime(request.form['publish_date'], '%Y-%m-%d') if request.form['publish_date'] else None
            paper.author_order = int(request.form['author_order']) if request.form['author_order'] else 1
            paper.is_corresponding = 'is_corresponding' in request.form
            paper.doi = request.form['doi']
            paper.abstract = request.form['abstract']
            paper.keywords = request.form['keywords']
            paper.teacher_id = request.form['teacher_id']
            
            db.session.commit()
            flash('论文信息更新成功！')
            return redirect(url_for('papers.paper_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}')
    
    return render_template('papers/edit.html', 
                          paper=paper,
                          teachers=teachers,
                          paper_levels=paper_levels)

@papers.route('/delete/<int:id>')
@login_required
def paper_delete(id):
    try:
        paper = Paper.query.get_or_404(id)
        db.session.delete(paper)
        db.session.commit()
        flash('论文信息删除成功！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}')
    return redirect(url_for('papers.paper_list'))