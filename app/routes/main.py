from flask import Blueprint, render_template
from ..models.book import Book

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    書籍列表首頁。
    取得所有書籍資料並渲染至 index.html。
    """
    books = Book.get_all()
    return render_template('index.html', books=books)
