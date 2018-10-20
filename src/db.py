from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    subtasks = db.relationship('Subtask', cascade='delete')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.done = kwargs.get('done', False)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'done': self.done
        }

class Subtask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.done = kwargs.get('done', False)
        self.task_id = kwargs.get('task_id')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'done': self.done
        }
