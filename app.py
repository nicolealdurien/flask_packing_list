from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import Model, SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  needed = db.Column(db.Boolean)
  packed = db.Column(db.Boolean)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  necessary = db.Column(db.Boolean)
  complete = db.Column(db.Boolean)


@app.route('/')
def index():
  #show all items and todos
  item_list = Entry.query.order_by(Entry.title).all()
  todo_list = Todo.query.order_by(Todo.title).all()
  return render_template('base.html', item_list=item_list, todo_list=todo_list)

@app.route('/add-item', methods=['POST'])
def add_item():
  #add new item entry
  title = request.form.get("title")
  new_entry = Entry(title=title, needed=True, packed=False)
  db.session.add(new_entry)
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/add-todo', methods=['POST'])
def add_todo():
  #add new todo entry
  title = request.form.get("title")
  new_entry = Todo(title=title, necessary=True, complete=False)
  db.session.add(new_entry)
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_packed/<int:entry_id>')
def toggle_packed(entry_id):
  #query db for id and modify packed boolean
  entry = Entry.query.filter_by(id=entry_id).first()
  entry.packed = not entry.packed
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_complete/<int:todo_id>')
def toggle_complete(todo_id):
  #query db for id and modify packed boolean
  todo = Todo.query.filter_by(id=todo_id).first()
  todo.complete = not todo.complete
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_needed/<int:entry_id>')
def toggle_needed(entry_id):
  #query db for id and modify needed boolean
  entry = Entry.query.filter_by(id=entry_id).first()
  entry.needed = not entry.needed
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_necessary/<int:todo_id>')
def toggle_necessary(todo_id):
  #query db for id and modify needed boolean
  todo = Todo.query.filter_by(id=todo_id).first()
  todo.necessary = not todo.necessary
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/delete-item/<int:entry_id>')
def delete_item(entry_id):
  #query db for id and delete item
  entry = Entry.query.filter_by(id=entry_id).first()
  db.session.delete(entry)
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/delete-task/<int:todo_id>')
def delete_task(todo_id):
  #query db for id and delete item
  todo = Todo.query.filter_by(id=todo_id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for("index"))


if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)