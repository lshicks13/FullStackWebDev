from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, Response, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate
from livereload import Server

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db_type = 'postgresql'
username = 'postgres'
password = 'secret123'
server = 'localhost'
port = '5432'
db_name = 'todoapp'

app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_type}://' \
                                        f'{username}:{password}@' \
                                        f'{server}:{port}/' \
                                        f'{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey
                        ('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


@app.route('/todos/<todo_id>/delete', methods=['DELETE', 'GET'])
def delete_todo(todo_id):
    error = False
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        # response = Response(status=303)
        # response.location = '/'
        # print(response)
        # return response
        return jsonify({
            'success': True
        })


@app.route('/todolists/<todolist_id>/set-completed', methods=['POST'])
def set_completed_todolist(todolist_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todolist = TodoList.query.get(todolist_id)
        todolist.completed = completed
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for('index'))


@app.route('/todolists/create', methods=['POST'])
def create_todolist():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name'] = todolist.name
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todolists')
def get_lists():
    return render_template('index.html',
                           data=TodoList.query.order_by('id').all())


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', data=Todo.query.filter_by
                           (list_id=list_id).order_by('id').all())


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
    app.run()
