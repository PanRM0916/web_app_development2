from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.book import Book
from ..models.tag import Tag

book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    新增書籍。
    GET: 顯示新增表單。
    POST: 處理表單提交並存入資料庫。
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        total_pages = request.form.get('total_pages', 0)
        status = request.form.get('status', '未讀')
        tags_str = request.form.get('tags', '')

        if not title:
            flash('書名為必填欄位！', 'danger')
            return render_template('book_form.html', book=None)

        book = Book.create(
            title=title,
            author=author,
            isbn=isbn,
            total_pages=int(total_pages) if total_pages else 0,
            status=status
        )

        if book:
            # 處理標籤
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                for name in tag_names:
                    tag = Tag.get_or_create(name=name)
                    book.tags.append(tag)
                from ..models import db
                db.session.commit()
            
            flash(f'成功新增書籍：{title}', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('新增書籍失敗，請稍後再試。', 'danger')

    return render_template('book_form.html', book=None)

@book_bp.route('/<int:id>')
def book_detail(id):
    """
    書籍詳情頁面。
    顯示特定書籍的詳細資訊與筆記列表。
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('main.index'))
    return render_template('book_detail.html', book=book)

@book_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    """
    編輯書籍資訊。
    GET: 顯示預填資料的編輯表單。
    POST: 更新資料庫中的書籍資訊。
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        total_pages = request.form.get('total_pages', 0)
        current_page = request.form.get('current_page', 0)
        status = request.form.get('status')
        tags_str = request.form.get('tags', '')

        if not title:
            flash('書名為必填欄位！', 'danger')
            return render_template('book_form.html', book=book)

        updated_book = book.update(
            title=title,
            author=author,
            isbn=isbn,
            total_pages=int(total_pages) if total_pages else 0,
            current_page=int(current_page) if current_page else 0,
            status=status
        )

        if updated_book:
            # 更新標籤 (簡單處理：清空再重新加入)
            book.tags = []
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                for name in tag_names:
                    tag = Tag.get_or_create(name=name)
                    book.tags.append(tag)
            from ..models import db
            db.session.commit()

            flash('書籍資訊已更新。', 'success')
            return redirect(url_for('book.book_detail', id=id))

    # 準備標籤字串供編輯顯示
    tags_str = ', '.join([t.name for t in book.tags])
    return render_template('book_form.html', book=book, tags_str=tags_str)

@book_bp.route('/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除書籍。
    從資料庫移除書籍及其關聯的所有筆記。
    """
    book = Book.get_by_id(id)
    if book:
        title = book.title
        if book.delete():
            flash(f'已刪除書籍：{title}', 'info')
        else:
            flash('刪除失敗。', 'danger')
    return redirect(url_for('main.index'))
