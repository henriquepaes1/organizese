import sqlite3

df = sqlite3.connect('tasks.db')
cursor_task = df.cursor()

cursor_task.execute("CREATE TABLE tasks(task_id INTEGER, user_id INTEGER, desc TEXT, PRIMARY KEY (task_id) FOREIGN KEY (user_id) REFERENCES users(id))")