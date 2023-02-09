from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# making app context, not in tutorial but necessary to get it to work, from stackoverflow:
# https://stackoverflow.com/a/74364913

app.app_context().push()
# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# hone route, this is the main page, which is why there is nothing after the slash, will redirect to this homepage when starting


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

# now we add the operations we want for each of the todos, we do this by adding a new route that performs the operation,
# including reflecting that change in the db, and then redirects to homepage.

# route for adding a todo


def add():
    # getting name of todo from form
    title = request.form.get("title")
    # making todo item according to class
    new_todo = Todo(title=title, complete=False)
    # adding todo to DB
    db.session.add(new_todo)
    db.session.commit()
    # redirectign to home to show new todo in list
    return redirect(url_for("home"))


# route for updating todo (aka making completed or uncompleted)
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # get the specific todo associated with the button pressed
    todo = Todo.query.filter_by(id=todo_id).first()
    # if done, will mark not done, and if not done, will mark done
    todo.complete = not todo.complete
    # save to DB
    db.session.commit()
    return redirect(url_for("home"))

# route to delete todo


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # get the specific todo associated with the button pressed
    todo = Todo.query.filter_by(id=todo_id).first()

    # delete in DB
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
