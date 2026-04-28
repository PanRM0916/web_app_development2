from datetime import datetime
from . import db

# 多對多關聯表：書籍與標籤
book_tags = db.Table('book_tags',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    isbn = db.Column(db.String(20))
    total_pages = db.Column(db.Integer, default=0)
    current_page = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), nullable=False, default='未讀')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯：一對多 (書籍 -> 筆記)
    notes = db.relationship('Note', backref='book', lazy=True, cascade="all, delete-orphan")
    # 關聯：多對多 (書籍 -> 標籤)
    tags = db.relationship('Tag', secondary=book_tags, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return f'<Book {self.title}>'

    # CRUD 方法
    @classmethod
    def create(cls, **kwargs):
        """
        新增一筆書籍記錄。
        """
        try:
            book = cls(**kwargs)
            db.session.add(book)
            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            print(f"Error creating book: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有書籍記錄。
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """
        根據 ID 取得單筆書籍記錄。
        """
        return cls.query.get(id)

    def update(self, **kwargs):
        """
        更新書籍記錄。
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating book: {e}")
            return None

    def delete(self):
        """
        刪除書籍記錄。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting book: {e}")
            return False
