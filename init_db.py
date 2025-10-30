from app import create_app
from app.models import db, User, init_dict_data
from app import bcrypt

# 创建应用实例
app = create_app('development')

# 在应用上下文中初始化数据库
with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 初始化字典数据
    init_dict_data()
    
    # 检查是否已经有用户数据
    if User.query.count() == 0:
        # 创建管理员用户
        admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@example.com', password=admin_password)
        db.session.add(admin)
        
        # 创建一些示例用户
        usernames = ['alice', 'bob', 'charlie', 'david', 'eve']
        for username in usernames:
            password = bcrypt.generate_password_hash(f'{username}123').decode('utf-8')
            user = User(username=username, email=f'{username}@example.com', password=password)
            db.session.add(user)
        
        # 提交用户数据
        db.session.commit()
        print(f'已成功创建 {len(User.query.all())} 个用户。')
    else:
        print('数据库中已有用户数据，跳过用户初始化步骤。')