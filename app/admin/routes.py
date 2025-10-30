from flask import render_template, redirect, url_for, flash, send_file
import pandas as pd
import io
from flask_login import login_required, current_user
from . import admin
from ..models import User,  db

# 简单的管理员检查装饰器
def admin_required(func):
    def wrapper(*args, **kwargs):
        # 简单的管理员判断，假设用户名admin是管理员
        if not current_user.is_authenticated or current_user.username != 'admin':
            flash('您没有管理员权限')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    # 统计发布博客最多的前10位用户
    top_users = db.session.query(
        User.username,
        db.func.count(Post.id).label('post_count')
    ).join(Post).group_by(User.username).order_by(db.text('post_count DESC')).limit(10).all()
    
    # 获取所有用户和文章总数
    total_users = User.query.count()
    total_posts = Post.query.count()
    
    return render_template('admin/dashboard.html', 
                          top_users=top_users,
                          total_users=total_users,
                          total_posts=total_posts)

# @admin.route('/admin/export_top_users')
# @login_required
# @admin_required
# def export_top_users():
#     # 获取发布博客最多的前10位用户数据
#     top_users = db.session.query(
#         User.username,
#         db.func.count(Post.id).label('post_count')
#     ).join(Post).group_by(User.username).order_by(db.text('post_count DESC')).limit(10).all()
    
#     # 创建DataFrame
#     data = {
#         '排名': [i+1 for i in range(len(top_users))],
#         '用户名': [user.username for user in top_users],
#         '文章数量': [user.post_count for user in top_users]
#     }
#     df = pd.DataFrame(data)
    
#     # 创建Excel文件
#     output = io.BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Top Users')
#     output.seek(0)
    
#     # 发送文件供下载
#     return send_file(output, 
#                      download_name='top_users_blog_posts.xlsx',
#                      as_attachment=True,
#                      mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')