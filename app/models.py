from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.extansions import db


class Tasks(db.Model):  # ignore: typing
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    description = Column(String(200))
    status = Column(String(30))
    created_on = Column(DateTime, default=datetime.now)
    dead_line = Column(DateTime, nullable=True)
    done_on = Column(DateTime, nullable=True)

    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    delete_on = Column(DateTime, default=None, nullable=True)
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    parent = relationship("Tasks", remote_side=[id], backref="children")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("Users", back_populates="tasks")


class Users(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    created_on = Column(DateTime, default=datetime.now)
    delete_on = Column(DateTime, default=None, nullable=True)
    tasks = relationship("Tasks", back_populates="user")
    categories = relationship("Category", back_populates="user")

    def __str__(self):
        return f"<Users {self.id}>"

    def __repr__(self):
        return f"<Users {self.id}>"


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    created_on = Column(DateTime, default=datetime.now)
    delete_on = Column(DateTime, default=None, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    tasks = relationship("Tasks", lazy=False)
    user = relationship("Users", back_populates="categories")
