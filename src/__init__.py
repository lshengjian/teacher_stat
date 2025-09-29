# my_app/__init__.py
from flask import Flask
from .models import db # 从同级目录的 models.py 导入 db

def create_app(database_uri='sqlite:///./teachers.db'):
    """
    应用工厂函数
    """
    app = Flask('main', static_folder='static', static_url_path='/static')
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. 使用 db.init_app() 将 db 对象与 app 实例关联起来
    #    这一步会读取 app.config 中的数据库配置，并完成所有设置。
    db.init_app(app)

    # (可选) 在这里可以注册蓝图、添加其他扩展等
    # from . import views
    # app.register_blueprint(views.bp)

    return app