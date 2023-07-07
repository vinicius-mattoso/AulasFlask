# Import Libs
import os
import sqlite3

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length




# Making a test to see if the .db existis, and than create or just to be used
connection = sqlite3.connect("teste.db")

# Getting the cursos from the connection
cursor = connection.cursor()

# Exceuting the code to create a .db with the ID column
cursor.execute("CREATE TABLE IF NOT EXISTS teste (id TEXT)")

cursor.close() 


basedir = os.path.abspath(os.path.dirname(__file__))

print(f'Esse é meu basedir : {basedir}')

# instance the Flask, to generate the app
app = Flask (__name__)

# configure the SQLite database, relative to the app instance folder
# creating a simple database
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///d2b.sqlite3"

# To create a SQLite database in a specific path
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database2.sqlite3')

# Creating an Automatic db creator using a specifc path, with a warning msg in terminal
number = ''
db_name = f'database{number}.sqlite3'

db_path = os.path.join(basedir, db_name)

if os.path.exists(db_path):
    print("O .db Já existe!")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, db_name)}'
else:
    print('VAMOS CRIAR O .DB')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, db_name)}'

# Insert the key from the .db
app.config['SECRET_KEY'] = ' 73bbf3a3e7f149bcbfa4fa37a981b8fc'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the extension
db = SQLAlchemy(app)

# Creating a simple db for the todo app
class Todo(db.Model):
    # identity column
    id = db.Column(db.Integer, primary_key=True)
    # todo text - > nullable = False means that can not be empty
    todo = db.Column(db.String(50), nullable=False)

# Creating the form from the app
class TodoForm(FlaskForm):
    todo = StringField('Enter todo:', validators=[InputRequired(),Length(min = 4, max = 50)])
    submit = SubmitField('Add todo')


# Creating Routes for the app

@app.route('/', methods=['GET',"POST"])
def home():
    # To return just a simple string 
    # return " Hello from Flask"

    # To return a render page
    # return render_template('home.html')

    # To return a render page now with the form
    form = TodoForm()
    # Acess the todo dataset table
    todos = Todo.query.all()

    # Check if has a update
    if form.validate_on_submit():
        # Create a new todo object
        new_todo = Todo(todo=form.todo.data)
        # Add the new object to the database
        db.session.add(new_todo)
        # Save the changes in the database
        db.session.commit()

        # after add return for the home page to avoid problems
        return redirect(url_for('home'))

    # This is not showing the list of todos
    # return render_template('home.html', form=form)

    # Passing the list of todos
    return render_template('home.html', form=form, todos=todos)

@app.route('/complete-todo/<int:todo_id>', methods=['GET',"POST"])
def complete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

# Making the app running
if __name__ == '__main__':
    # in case of deploy debug should be False

    # By default the port is in 127.0.0.1:5000
    # app.run(debug = True)

    # To change the port 
    # app.run(debug = True, port = 8000)

    # To change the port but consider the localhost as the host
    # app.run(debug = True, host = "localhost", port = 8000)

    # To create the database automatically when the Flask app is initialized
    app.app_context().push()
    db.create_all()
    
    # Now if you want a specific host
    app.run(debug = True, host = "127.0.0.1" , port = 8000)