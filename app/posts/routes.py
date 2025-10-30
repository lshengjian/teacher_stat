from flask import render_template, redirect, url_for, flash, request
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import posts
from ..models import Post, User, db
from datetime import datetime

@posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空')
            return redirect(url_for('posts.new_post'))
        
        new_post = Post(title=title, content=content, author=current_user)
        
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('文章发布成功')
            return redirect(url_for('posts.user_posts', username=current_user.username))
        except:
            db.session.rollback()
            flash('发布失败，请稍后再试')
            return redirect(url_for('posts.new_post'))
    
    return render_template('posts/new_post.html')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post)

@posts.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash('您没有权限编辑这篇文章')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空')
            return redirect(url_for('posts.edit_post', post_id=post_id))
        
        post.title = title
        post.content = content
        post.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('文章已更新')
            return redirect(url_for('posts.post', post_id=post_id))
        except:
            db.session.rollback()
            flash('更新失败，请稍后再试')
            return redirect(url_for('posts.edit_post', post_id=post_id))
    
    return render_template('posts/edit_post.html', post=post)

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        flash('您没有权限删除这篇文章')
        return redirect(url_for('main.index'))
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('文章已删除')
    except:
        db.session.rollback()
        flash('删除失败，请稍后再试')
    
    return redirect(url_for('posts.user_posts', username=current_user.username))

@posts.route('/user/<string:username>')
def user_posts(username):
    # 首先直接查询用户是否存在，而不是通过文章查询
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('用户不存在')
        return redirect(url_for('main.index'))
    
    # 查询该用户的所有文章，使用正确的外键字段名user_id
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('posts/user_posts.html', posts=posts, username=username)