import os
from flask import Flask
from .models import db
from .routes.main import main_bp
from .routes.book import book_bp
from .routes.note import note_bp

def create_app():
    app = Flask(__name__)
    
    # 載入設定
    app.config.from_object('config.Config')
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化擴充套件
    db.init_app(app)

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(note_bp)

    return app

def init_db():
    """
    初始化資料庫 (由 Step 6.5 使用)
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        print("資料庫初始化成功！")
