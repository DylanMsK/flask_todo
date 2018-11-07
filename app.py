from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *

app = Flask(__name__)


# db 설정
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todo'   # 초기에 DB create 할때 지정한 db이름 todo
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.deadline).all()
    return render_template('index.html', todos=todos)
    
# @app.route('/posts/new')
# def new():
#     return render_template('new.html')
    
# @app.route('/posts/create', methods=['POST'])
# def create():
#     # 사용자가 입력한 데이터 가져오기
#     todo = request.form['todo']
#     deadline = request.form.get('deadline')
#     # 가져온 데이터로 todo 만들기
#     new_todo = Todo(todo=todo, deadline=deadline)
#     # todo DB에 저장하기
#     db.session.add(new_todo)
#     db.session.commit()
#     return redirect('/')

# 위의 new와 create를 하나로 합침
@app.route('/todo/create', methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        todo = Todo(request.form['todo'], request.form['deadline'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('new.html')

# @app.route('/todo/<int:id>/edit')
# def edit(id):
#     origin_todo = Todo.query.get(id)
#     return render_template('edit.html', todo=origin_todo)

# @app.route('/todo/<int:id>/update', methods=['POST'])
# def update(id):
#     origin_todo = Todo.query.get(id)
#     origin_todo.todo = request.form['todo']
#     origin_todo.deadline = request.form['deadline']
#     db.session.commit()
#     return redirect('/')

@app.route('/todo/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    post_todo = Todo.query.get(id)
    if request.method == 'POST':
        post_todo.todo = request.form['todo']
        post_todo.deadline = request.form['deadline']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=post_todo)

@app.route('/todo/<int:id>/delete')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    