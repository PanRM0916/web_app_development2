from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    書籍列表首頁。
    取得所有書籍資料並渲染至 index.html。
    """
    pass
