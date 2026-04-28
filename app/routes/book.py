from flask import Blueprint, render_template, request, redirect, url_for

book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    新增書籍。
    GET: 顯示新增表單。
    POST: 處理表單提交並存入資料庫。
    """
    pass

@book_bp.route('/<int:id>')
def book_detail(id):
    """
    書籍詳情頁面。
    顯示特定書籍的詳細資訊與筆記列表。
    """
    pass

@book_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    """
    編輯書籍資訊。
    GET: 顯示預填資料的編輯表單。
    POST: 更新資料庫中的書籍資訊。
    """
    pass

@book_bp.route('/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除書籍。
    從資料庫移除書籍及其關聯的所有筆記。
    """
    pass
