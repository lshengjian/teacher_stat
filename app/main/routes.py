from flask import render_template
from . import main
from ..models import Teacher, Project, Paper, init_dict_data, db
from flask import current_app

@main.route('/')
def index():
    # 初始化字典数据
    with current_app.app_context():
        init_dict_data()
    
    # 统计信息
    teacher_count = Teacher.query.count()
    project_count = Project.query.count()
    paper_count = Paper.query.count()
    
    return render_template('main/index.html', 
                          teacher_count=teacher_count,
                          project_count=project_count,
                          paper_count=paper_count)

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/statistics')
def statistics():
    # 获取统计数据
    teachers = Teacher.query.all()
    
    # 按职称统计
    position_stats = {}
    for teacher in teachers:
        position_name = teacher.position.name if teacher.position else '未知'
        position_stats[position_name] = position_stats.get(position_name, 0) + 1
    
    # 项目统计
    projects_by_level = {}
    projects = Project.query.all()
    for project in projects:
        level_name = project.project_level.name if project.project_level else '未知'
        projects_by_level[level_name] = projects_by_level.get(level_name, 0) + 1
    
    # 论文统计
    papers_by_level = {}
    papers = Paper.query.all()
    for paper in papers:
        level_name = paper.paper_level.name if paper.paper_level else '未知'
        papers_by_level[level_name] = papers_by_level.get(level_name, 0) + 1
    
    return render_template('main/statistics.html',
                          position_stats=position_stats,
                          projects_by_level=projects_by_level,
                          papers_by_level=papers_by_level)