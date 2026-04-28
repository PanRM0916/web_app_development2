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
        """
        建立新標籤。
        """
        try:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            print(f"Error creating tag: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有標籤。
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """
        根據 ID 取得標籤。
        """
        return cls.query.get(id)

    @classmethod
    def get_or_create(cls, name):
        """
        取得標籤，若不存在則建立。
        """
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = cls.create(name=name)
        return tag

    def delete(self):
        """
        刪除標籤。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting tag: {e}")
            return False
