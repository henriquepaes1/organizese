from flask import Flask, redirect, render_template, request, session

from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from tempfile import mkdtemp

import sqlite3

# Session settings from Flask

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "seila123456"
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False

Session(app)

if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"

#  Set tools to use SQLite Database

db = sqlite3.connect('users.db', check_same_thread=False)
cursor = db.cursor()

df = sqlite3.connect('tasks.db', check_same_thread=False)
cursor_task = df.cursor()

df_conc = sqlite3.connect('concluded.db', check_same_thread=False)
cursor_conclude = df_conc.cursor()

# Lists to check passwords

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
           'z']

@app.route("/")
def index():
    return redirect("/login")  # Default route asks users to log in

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # User clicked in Register button
        # Get info from HTML form
        user = request.form.get("username")
        first_password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check the database
        check_username = cursor.execute(
            "SELECT * FROM users WHERE username = ?", [user])  # use list

        if len(check_username.fetchall()) != 0:
            return("Username already exists")

        if first_password != confirmation:
            return("Passwords do not match")
        # check if password is adequate
        condition1 = 0
        condition2 = 0

        for i in first_password:
            if i in letters:
                condition1 = 1
            elif i in numbers:
                condition2 = 1

        if condition1 == 1 and condition2 == 1:
            password = generate_password_hash(first_password)
            cursor.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", (user, password))

            db.commit()  # Save changes in database
            db.close()  # avoid SQL memory leaks
            return redirect("/login")  # ask new user to log in
        else:
            return("Password must contain letters and numbers")

    else:  # user is just viewing the page
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        user = request.form.get("username")
        password = request.form.get("password")

        if not user:
            return("Provide an username")
        elif not password:
            return("Provide password")
        
        db_check = cursor.execute("SELECT * FROM users WHERE username=?", [user])
        db_check_dict = db_check.fetchall()  # Return list, as every username is unique, only one list


        if len(db_check_dict) != 1 or not check_password_hash(db_check_dict[0][2], password):
            return("invalid username or password")

        session["user_id"] = db_check_dict[0][0]  # starts session, which will be identification
        return redirect("/see_tasks")  # take user to his saved tasks
    
    else:
        return render_template("login.html")

@app.route("/see_tasks", methods=['GET', 'POST'])
def see_tasks():
    if request.method == 'POST': # user clicked in add tasks
        if request.form['submit_button'] == 'add':
            return redirect('/add_tasks')

        elif request.form['submit_button'] == 'delete':
            task = request.form['task_id'] # task to be dropped
            print(task)
            cursor_task.execute("DELETE FROM tasks WHERE task_id =? AND user_id=?", (task, session['user_id']))
            sql_desc = cursor_task.execute("SELECT * FROM tasks WHERE user_id=?", (session['user_id'],))
            descs = sql_desc.fetchall()  # retorna tuplas 
            df.commit()
            return render_template('see_tasks.html', descs=descs)

        elif request.form['submit_button'] == 'conclude':
            task = request.form['task_id'] # task to be concluded
            print(task)
            task_data = cursor_task.execute("SELECT * FROM tasks WHERE user_id=? AND task_id=?", (session['user_id'], task))
            desc = task_data.fetchall()[0][2]
            cursor_conclude.execute("INSERT INTO concluded (user_id, desc) VALUES(?, ?)", (session['user_id'], desc))
            # insert into concluded data base
            cursor_task.execute("DELETE FROM tasks WHERE task_id =? AND user_id=?", (task, session['user_id']))
            df_conc.commit() # update concluded database
            df.commit() # update tasks data base
            return redirect("/concluded")

    else:  # user is just looking at his tasks
        sql_desc = cursor_task.execute("SELECT * FROM tasks WHERE user_id=?", (session['user_id'],))
        descs = sql_desc.fetchall()  # return tuples 
        if(len(descs) > 0):
            return render_template('see_tasks.html', descs=descs) # if user has saved tasks
        else:                  
            return render_template("see_tasks.html") # if user doesn't have tasks


@app.route("/add_tasks", methods=['GET', 'POST'])
def add_tasks():
    if request.method == 'POST': # user clicked to add tasks
        description = request.form.get("desc")
        cursor_task.execute("INSERT INTO tasks (user_id, desc) VALUES(?, ?)", (session['user_id'], description))
        df.commit()
        return redirect("/see_tasks")
    else:
        return render_template("add_tasks.html")

@app.route("/concluded", methods=['GET', 'POST'])
def concluded():
    if request.method == 'POST':
        return redirect("/add_tasks")
    else:
        concluded_tasks = cursor_conclude.execute("SELECT * FROM concluded WHERE user_id=?", (session['user_id'],))
        concluded_html = concluded_tasks.fetchall()
        return render_template("concluded.html", descs=concluded_html)