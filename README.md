# Flask博客系统

这是一个使用Flask和SQLite3开发的多用户博客系统。用户可以注册账号，发布、编辑和删除自己的博客文章，管理员可以查看统计数据。

## 功能特性

- 用户注册和登录
- 发布、编辑和删除博客文章
- 查看其他用户的博客文章
- 管理员可以查看统计数据，包括发布博客最多的前10位用户

## 技术栈

- 后端：Flask, SQLAlchemy
- 数据库：SQLite3
- 前端：HTML, CSS

## 安装指南

1. 克隆仓库

```bash
git clone <repository-url>
cd study-flask
```

2. 创建虚拟环境

```bash
python -m venv venv
```

3. 激活虚拟环境

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. 安装依赖

```bash
pip install -r requirements.txt
```

5. 运行应用

```bash
python run.py
```

应用将在 http://localhost:5000 启动。

## 默认管理员账号

首次运行应用时，会自动创建一个管理员账号：
- 用户名: admin
- 密码: admin123

请在首次登录后修改密码以确保安全。

## 项目结构

```
study-flask/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── config.py            # 配置文件
│   ├── models.py            # 数据库模型
│   ├── main/                # 主页蓝图
│   ├── auth/                # 认证蓝图
│   ├── posts/               # 博客文章蓝图
│   ├── admin/               # 管理员蓝图
│   └── templates/           # HTML模板
├── run.py                   # 应用入口
├── requirements.txt         # 项目依赖
└── .gitignore               # Git忽略文件
```

## 开发说明

- 本项目使用Flask的蓝图(Blueprint)来组织代码，提高代码的可维护性
- 数据库使用SQLite3，适合小型应用和开发环境
- 所有用户密码都经过bcrypt加密存储
- 项目结构清晰，便于扩展和维护