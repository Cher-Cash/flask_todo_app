from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extansions import db


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    description = Column(String(200))
    status = Column(String(30))
    created_on = Column(DateTime, default=datetime.now)
    dead_line = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    delete_on = Column(DateTime, default=None, nullable=True)
    parent_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    parent = relationship("Tasks", remote_side=[id], backref='children')


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    created_on = Column(DateTime, default=datetime.now)
    delete_on = Column(DateTime, default=None, nullable=True)
    tasks = relationship('Tasks', backref='tasks', lazy=False)


class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    created_on = Column(DateTime, default=datetime.now)
    delete_on = Column(DateTime, default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tasks = relationship('Tasks', lazy=False)
