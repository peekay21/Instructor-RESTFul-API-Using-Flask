from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()
db = SQLAlchemy()


class Instructor(db.Model):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    dept_name = db.Column(db.String)
    salary = db.Column(db.Integer)

    def __repr__(self):
        return f'<Instructor {self.id}>'

