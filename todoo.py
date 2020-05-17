from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Pc/Desktop/PYTHON_2_BOLUM/2TodooApp_186_Todoo/todoo.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    todos =Todo.query.all()  #todolar buraya sözlük yapısıyla gelecek
    return render_template("index.html",todos=todos)

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()  #bu id deki ilk degeri alsın dedik ama zaten her id den bir tane olacak
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete
    
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add",methods = ["post"])
def addTodo():
    title = request.form.get("title")   #index.html den title verisini alıyoruz.
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)   #olusan objeyi ekliyoruz.
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)     #primary_key=True primary key olsun ve auto increment olarak artsın
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)