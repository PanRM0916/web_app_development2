from . import db

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Tag {self.name}>'

    # CRUD 方法
    @classmethod
    def create(cls, name):
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_create(cls, name):
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = cls.create(name=name)
        return tag

    def delete(self):
        db.session.delete(self)
        db.session.commit()
