import json
from db import db, Task, Subtask
from flask import Flask, request

db_filename = "todo.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    
@app.route('/')
@app.route('/tasks/')
def get_tasks():
    tasks = Task.query.all()
    res = {'success': True, 'data': [task.serialize() for task in tasks]} 
    return json.dumps(res), 200

@app.route('/tasks/', methods=['POST'])
def create_task():
    post_body = json.loads(request.data)

    task = Task(
        description=post_body.get('description'),
        done=bool(post_body.get('done'))
    )
    db.session.add(task)
    db.session.commit()
    return json.dumps({'success': True, 'data': task.serialize()}), 201

@app.route('/tasks/<int:task_id>/')
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first() 
    if task is not None:
        return json.dumps({'success': True, 'data': task.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404

@app.route('/tasks/<int:task_id>/', methods=['POST'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is not None:
        post_body = json.loads(request.data)
        task.description = post_body.get('description', task.description)
        task.done = bool(post_body.get('done', task.done))
        db.session.commit()
        return json.dumps({'success': True, 'data': task.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404

@app.route('/tasks/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first() 
    if task is not None:
        db.session.delete(task)
        db.session.commit()
        return json.dumps({'success': True, 'data': task.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404 

@app.route('/tasks/<int:task_id>/subtasks/')
def get_subtasks(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is not None:
        subtasks = [subtask.serialize() for subtask in task.subtasks]
        return json.dumps({'success': True, 'data': subtasks}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404 

@app.route('/tasks/<int:task_id>/subtasks/', methods=['POST'])
def create_subtask(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is not None:
        post_body = json.loads(request.data)
        subtask = Subtask(
            description=post_body.get('description'),
            done=bool(post_body.get('done')),
            task_id=task.id
        )
        task.subtasks.append(subtask)
        db.session.add(subtask)
        db.session.commit()
        return json.dumps({'success': True, 'data': subtask.serialize()})
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
