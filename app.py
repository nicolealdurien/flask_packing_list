from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  needed = db.Column(db.Boolean)
  packed = db.Column(db.Boolean)


@app.route('/')
def index():
  #show all items
  item_list = Item.query.all()
  return render_template('base.html', item_list=item_list)

@app.route('/add', methods=['POST'])
def add():
  #add new item
  title = request.form.get("title")
  new_item = Item(title=title, needed=True, packed=False)
  db.session.add(new_item)
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_packed/<int:item_id>')
def toggle_packed(item_id):
  #query db for id and modify packed boolean
  item = Item.query.filter_by(id=item_id).first()
  item.packed = not item.packed
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/toggle_needed/<int:item_id>')
def toggle_needed(item_id):
  #query db for id and modify packed boolean
  item = Item.query.filter_by(id=item_id).first()
  item.needed = not item.needed
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/delete/<int:item_id>')
def delete(item_id):
  #query db for id and delete item
  item = Item.query.filter_by(id=item_id).first()
  db.session.delete(item)
  db.session.commit()
  return redirect(url_for("index"))


if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)