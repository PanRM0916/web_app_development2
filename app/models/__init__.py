from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 匯入所有 Model 方便外部使用
from .book import Book
from .note import Note
from .tag import Tag
