from app import create_app, init_db

app = create_app()

if __name__ == '__main__':
    # 這裡可以加入初始化資料庫的檢查或其他邏輯
    app.run(debug=True)
