# TODO

## 프로젝트 폴더 생성

`$ mkdir todo`



## app과 model 파일 생성

`$ touch app.py`
`$ touch models.py`

- #### models.py

  ```python
  from flask_sqlalchemy import SQLAlchemy
  
  db = SQLAlchemy()
   
  class Todo(db.Model):
      __tablename__ = 'todos'
      id = db.Column(db.Integer, primary_key=True)
      todo = db.Column(db.String, nullable=False)
      deadline = db.Column(db.DateTime, nullable=False)
      
      def __init__(self, todo, deadline):
          self.todo = todo
          self.deadline = deadline
  ```

- #### app.py

  ```python
  from flask import Flask, render_template, request
  from flask_sqlalchemy import SQLAlchemy
  from flask_migrate import Migrate
  
  from models import *
  
  app = Flask(__name__)
  
  # db 설정
  app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todo'   # 초기에 DB create 할때 지정한 db이름 board
  # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
  app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
  db.init_app(app)
  migrate = Migrate(app, db)
  ```



## 기본 form 생성

`$ mkdir templates`
`$ touch templates/base.html`
`$ touch templates/index.html`

- #### base.html

  [bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/) 에서 기본 css와 js 가져오기

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>Document</title>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  </head>
  <body>
      <div class="tabs">
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a class="nav-link active" href="/">To Do</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/todos/create">New</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Completed</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Failed</a>
            </li>
          </ul>
      </div>
      <div class="container">
          {% block bb %}
          {% endblock %}
      </div>
      <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </body>
  </html>
  ```

- #### index.html

  ```html
  {% extends 'base.html' %}
  {% block body_block %}
  	{% for todo in todos %}
  		<h3>{{todo.todo}}</h3>
  		<h5>{{todo.deadline}}</h5>
  	{% endfor %}
  {% endblock %}
  ```

- #### app.py

  ```python
  @app.route('/')
  def index():
      todos = Todo.query.order_by(Todo.deadline).all()
      return render_template('index.html', todos=todos)
  ```



## todolist 생성

`$ touch templates/new.html`

- #### new.html

  ```html
  {% extends 'base.html' %}
  {% block bb %}
      <form action='/todo/create' method='post'>
        <div class="form-group">
          <label for="todo">TO DO</label>
          <input name='todo' type="text" class="form-control" id="todo" placeholder="할일을 적어주세요">
        </div>
        <div class="form-group">
          <label for="deadline">Deadline</label>
          <input name='deadline' type="date" class="form-control" id="deadline" >
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
  {% endblock %}
  ```

- #### app.py

  todo를 작성할 페이지를 보여주는 route와 작성한 todo를 DB에 저장할 route를 따로 생성

  ```python
  @app.route('/posts/new')
  def new():
      return render_template('new.html')
      
  @app.route('/posts/create', methods=['POST'])
  def create():
      # 사용자가 입력한 데이터 가져오기
      todo = request.form['todo']
      deadline = request.form.get('deadline')
      # 가져온 데이터로 todo 만들기
      new_todo = Todo(todo=todo, deadline=deadline)
      # todo DB에 저장하기
      db.session.add(new_todo)
      db.session.commit()
      return redirect('/')
  ```

  위의 두 route를 한 코드로 병합

  ```python
  @app.route('/todo/create', methods=['POST', 'GET'])
  def todo():
      if request.method == 'POST':
          todo = Todo(request.form['todo'], request.form['deadline'])
          db.session.add(todo)
          db.session.commit()
          return redirect('/')
      return render_template('new.html')
  ```

- #### index 페이지 수정

  ```html
  {% extends 'base.html' %}
  {% block bb %}
      {% for todo in todos %}
          <div class="jumbotron">
              <div class="row">
                  <div class="col">
                      <h3>{{todo.todo}}</h3>
                      <h5>{{todo.deadline.strftime('%Y년 %m월 %d일')}}</h5><br>
                  </div>
                  <div class="col">
                      <a href="/todo/{{todo.id}}/update" class="btn btn-outline-primary">수정</a>
                      <a href='/todo/{{todo.id}}/delete' class="btn btn-outline-success" onclick='return confirm("완료하시겠습니까?")'>완료</a>
                  </div>
              </div>
          </div>
      {% endfor %}
  {% endblock %}
  ```





## todolist 삭제

- #### app.py

  ```python
  @app.route('/todo/<int:id>/delete')
  def delete(id):
      todo = Todo.query.get(id)
      db.session.delete(todo)
      db.session.commit()
      return redirect('/')
  ```



## todolist 수정

- #### app.py

  ```python
  @app.route('/todo/<int:id>/update', methods=['POST', 'GET'])
  def update(id):
      post_todo = Todo.query.get(id)
      if request.method == 'POST':
          post_todo.todo = request.form['todo']
          post_todo.deadline = request.form['deadline']
          db.session.commit()
          return redirect('/')
      return render_template('update.html', todo=post_todo)
  ```

- #### update.html

  ```html
  {% extends 'base.html' %}
  {% block bb %}
      <form action='/todo/{{todo.id}}/update' method='post'>
        <div class="form-group">
          <label for="todo">TO DO</label>
          <input name='todo' type="text" class="form-control" id="todo" placeholder="할일을 적어주세요" value={{todo.todo}}>
        </div>
        <div class="form-group">
          <label for="deadline">Deadline</label>
          <!--<input name='deadline' type="date" class="form-control" id="deadline" value='{{todo.deadline.strftime("%Y-%m-%d")}}'>-->
          <input name='deadline' type="date" class="form-control" id="deadline" value={{todo.deadline}}>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
  {% endblock %}
  ```



## Heroku에 배포

- #### app.py

  ```python
  from flask import Flask, render_template, request
  from flask_sqlalchemy import SQLAlchemy
  from flask_migrate import Migrate
  
  from models import *
  import os
  
  app = Flask(__name__)
  
  # db 설정
  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
  app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
  db.init_app(app)
  migrate = Migrate(app, db)
  ```

- #### gunicorn 설치

  ```bash
  $ pip install gunicorn
  $ touch Procfile
  	web: gunicorn app:app
  $ gunicorn app:app		# 서버 실행 테스트
  ```

- #### heroku 세팅

  ```bash
  # $ export DATABASE_URL='postgresql:///todo' >> ~/.bashrc
  $ vi ~/.bashrc
  	 export DATABASE_URL='postgresql:///todo'	# 맨 마지막줄에 추가
  $ source ~/.bashrc	# 또는 exec $SHELL
  
  $ touch runtime.txt
  	python-3.6.1
  $ pip freeze > requirements.txt
  	python-editor 삭제
  ```

# heroku에 배포

- #### app.py

  ```python
  import os
  app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
  ```

  - Heroku 에서는 연결되는 DB가 DATABASE_URL이라는 환경변수로 지정되어 있음.
  - 만약 이렇게 변경하고 내 로컬 작업환경(혹은 C9)에서 문제가 되지 않으려면 환경변수 지정을 해줘야함.

  ```bash
  $ echo 'export DATABASE_URL="postgresql:///board"' >> ~/.bashrc
  $ source ~/.bashrc		# 또는 exec $SHELL
  ```


- #### gunicorn 설치

  ```bash
  $ pip install gunicorn
  $ touch Procfile
  	web: gunicorn app:app
  $ gunicorn app:app		# 서버 실행 테스트
  ```



- #### heroku 셋팅

  ```bash
  $ touch runtime.txt
  	python-3.6.1
  $ pip freeze > requirement
  ```

  - 필요없는 부분 삭제

    - pygobject

    - python-apt

    - python-editor

    - unattended-upgrades


- #### heroku 배포

  ```bash
  $ heroku login
  $ heroku create {프로젝트명}
  $ heroku git:clone -a {프로젝트명}
  $ git push heroku master
  
  $ heroku addons:create heroku-postgresql:hobby-dev	# heroku postgresql addon 설정
  $ heroku run flask db upgrade -a {프로젝트명}
  ```