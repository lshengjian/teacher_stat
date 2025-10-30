from app import create_app
from app.models import db, User
from app import bcrypt
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 在应用上下文中创建数据库表
with app.app_context():
    db.create_all()
    # 检查是否存在admin用户，如果不存在则创建
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', email='admin@example.com', password=admin_password)
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)