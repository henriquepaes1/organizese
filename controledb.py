
import sqlite3

db = sqlite3.connect('users.db')
cursor = db.cursor()

cursor.execute("CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id))")
