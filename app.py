# Import Libs
import os
import sqlite3

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

# Get the current directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# instance the Flask, to generate the app
app = Flask(__name__)

# Specify the new database path
db_path = os.path.join(basedir, 'new_database.db')

# Check if the new database exists
if os.path.exists(db_path):
    print("The new database already exists!")
else:
    print('Creating the new database...')
    # Create a connection to the new database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the necessary tables and insert initial data
    cursor.execute("CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, todo TEXT)")
    cursor.execute("INSERT INTO todo (todo) VALUES ('Sample Todo 1')")
    cursor.execute("INSERT INTO todo (todo) VALUES ('Sample Todo 2')")

    # Commit and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Insert the key for the new database
app.config['SECRET_KEY'] = '73bbf3a3e7f149bcbfa4fa37a981b8fc'

# Create the extension
db = SQLAlchemy(app)


# Creating a simple db for the todo app
class Todo(db.Model):
    # identity column
    id = db.Column(db.Integer, primary_key=True)
    # todo text -> nullable=False means that it cannot be empty
    todo = db.Column(db.String(50), nullable=False)


# Creating the form for the app
class TodoForm(FlaskForm):
    todo = StringField('Enter todo:', validators=[InputRequired(), Length(min=4, max=50)])
    submit = SubmitField('Add todo')


# Creating Routes for the app
@app.route('/', methods=['GET', 'POST'])
def home():
    form = TodoForm()
    todos = Todo.query.all()

    if form.validate_on_submit():
        new_todo = Todo(todo=form.todo.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('home.html', form=form, todos=todos)


@app.route('/complete-todo/<int:todo_id>', methods=['GET', 'POST'])
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

# New route for editing a todo
@app.route('/edit-todo/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm()

    if form.validate_on_submit():
        todo.todo = form.todo.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_todo.html', form=form, todo=todo)

# Running the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
