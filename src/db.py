from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    done = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.done = kwargs.get('done', False)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'done': self.done
        }