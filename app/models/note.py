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
        note = cls(**kwargs)
        db.session.add(note)
        db.session.commit()
        return note

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
