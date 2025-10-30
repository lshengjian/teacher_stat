from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, db
from .. import bcrypt

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 检查用户名和邮箱是否已存在
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        
        if user_by_username:
            flash('用户名已存在，请选择其他用户名')
            return redirect(url_for('auth.register'))
        
        if user_by_email:
            flash('邮箱已被注册，请使用其他邮箱')
            return redirect(url_for('auth.register'))
        
        # 创建新用户
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功，请登录')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('注册失败，请稍后再试')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('登录成功')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录')
    return redirect(url_for('main.index'))