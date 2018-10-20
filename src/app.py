import json
from db import db, Task
from flask import Flask, request

db_filename = "todo.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

@app.route('/')
@app.route('/tasks/')
def get_tasks():
    res = {'success': True, 'data': Db.get_all_tasks()}
    return json.dumps(res), 200

@app.route('/tasks/', methods=['POST'])
def create_task():
    post_body = json.loads(request.data)
    description = post_body['description']
    task = {
        'id': Db.insert_task_table(description, False),
        'description': description,
        'done': False
    }
    return json.dumps({'success': True, 'data': task}), 201

@app.route('/tasks/<int:task_id>/')
def get_task(task_id):
    task = Db.get_task_by_id(task_id)
    if task is not None:
        return json.dumps({'success': True, 'data': task}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404

@app.route('/tasks/<int:task_id>/', methods=['POST'])
def update_task(task_id):
    post_body = json.loads(request.data)
    description = post_body['description']
    done = bool(post_body['done'])
    Db.update_task_by_id(task_id, description, done)

    task = Db.get_task_by_id(task_id)
    if task is not None:
        return json.dumps({'success': True, 'data': task}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404

@app.route('/tasks/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
    task = Db.get_task_by_id(task_id)
    if task is not None:
        Db.delete_task_by_id(task_id)
        return json.dumps({'success': True, 'data': task}), 200
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
