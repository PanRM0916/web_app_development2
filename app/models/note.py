from datetime import datetime
from . import db

# 多對多關聯表：筆記與標籤
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯：多對多 (筆記 -> 標籤)
    tags = db.relationship('Tag', secondary=note_tags, backref=db.backref('notes', lazy='dynamic'))

    def __repr__(self):
        return f'<Note {self.id} for Book {self.book_id}>'

    # CRUD 方法
    @classmethod
    def create(cls, **kwargs):
        """
        針對特定書籍新增一筆筆記。
        """
        try:
            note = cls(**kwargs)
            db.session.add(note)
            db.session.commit()
            return note
        except Exception as e:
            db.session.rollback()
            print(f"Error creating note: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有筆記記錄。
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """
        根據 ID 取得單筆筆記記錄。
        """
        return cls.query.get(id)

    def update(self, **kwargs):
        """
        更新筆記內容。
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating note: {e}")
            return None

    def delete(self):
        """
        刪除筆記記錄。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting note: {e}")
            return False
