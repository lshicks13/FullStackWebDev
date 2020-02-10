from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sysconfig
from flask_migrate import Migrate

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
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


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


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


# if __name__ == '__main__':
#     app.run()
