from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.note import Note
from ..models.book import Book
from ..models.tag import Tag

note_bp = Blueprint('note', __name__)

@note_bp.route('/books/<int:book_id>/notes/add', methods=['GET', 'POST'])
def add_note(book_id):
    """
    針對特定書籍新增筆記。
    GET: 顯示新增筆記表單。
    POST: 處理表單提交並存入資料庫。
    """
    book = Book.get_by_id(book_id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        content = request.form.get('content')
        tags_str = request.form.get('tags', '')

        if not content:
            flash('筆記內容不能為空！', 'danger')
            return render_template('note_form.html', book=book, note=None)

        note = Note.create(book_id=book_id, content=content)
        if note:
            # 處理標籤
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                for name in tag_names:
                    tag = Tag.get_or_create(name=name)
                    note.tags.append(tag)
                from ..models import db
                db.session.commit()

            flash('筆記已成功新增。', 'success')
            return redirect(url_for('book.book_detail', id=book_id))
    
    return render_template('note_form.html', book=book, note=None)

@note_bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    """
    編輯筆記內容。
    GET: 顯示編輯表單。
    POST: 更新資料庫中的筆記內容。
    """
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該筆記。', 'warning')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        content = request.form.get('content')
        tags_str = request.form.get('tags', '')

        if not content:
            flash('筆記內容不能為空！', 'danger')
            return render_template('note_form.html', book=note.book, note=note)

        updated_note = note.update(content=content)
        if updated_note:
            # 更新標籤
            note.tags = []
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                for name in tag_names:
                    tag = Tag.get_or_create(name=name)
                    note.tags.append(tag)
            from ..models import db
            db.session.commit()

            flash('筆記已更新。', 'success')
            return redirect(url_for('book.book_detail', id=note.book_id))

    tags_str = ', '.join([t.name for t in note.tags])
    return render_template('note_form.html', book=note.book, note=note, tags_str=tags_str)

@note_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    刪除特定筆記。
    刪除後重導向回所屬書籍的詳情頁。
    """
    note = Note.get_by_id(id)
    if note:
        book_id = note.book_id
        if note.delete():
            flash('筆記已刪除。', 'info')
        else:
            flash('刪除失敗。', 'danger')
        return redirect(url_for('book.book_detail', id=book_id))
    return redirect(url_for('main.index'))
