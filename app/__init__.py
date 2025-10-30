from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import config
from .models import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .teachers import teachers as teachers_blueprint
    app.register_blueprint(teachers_blueprint, url_prefix='/teachers')
    
    from .projects import projects as projects_blueprint
    app.register_blueprint(projects_blueprint, url_prefix='/projects')
    
    from .papers import papers as papers_blueprint
    app.register_blueprint(papers_blueprint, url_prefix='/papers')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    # 初始化数据库
    with app.app_context():
        db.create_all()
    
    return app

# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))