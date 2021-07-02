from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  value = db.Column(db.String(128))
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  name = db.Column(db.String(32), unique=True)
  password = db.Column(db.String(32))
  tasks = db.relationship("Task")
