from flask import Blueprint, render_template, request, redirect, url_for

note_bp = Blueprint('note', __name__)

@note_bp.route('/books/<int:book_id>/notes/add', methods=['GET', 'POST'])
def add_note(book_id):
    """
    針對特定書籍新增筆記。
    GET: 顯示新增筆記表單。
    POST: 處理表單提交並存入資料庫。
    """
    pass

@note_bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    """
    編輯筆記內容。
    GET: 顯示編輯表單。
    POST: 更新資料庫中的筆記內容。
    """
    pass

@note_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    刪除特定筆記。
    刪除後重導向回所屬書籍的詳情頁。
    """
    pass
