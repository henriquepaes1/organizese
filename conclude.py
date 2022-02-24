import sqlite3

df_conc = sqlite3.connect('concluded.db') # initializes new db
cursor_conclude = df_conc.cursor()

cursor_conclude.execute("CREATE TABLE concluded(conc_task_id INTEGER, user_id INTEGER, desc TEXT, PRIMARY KEY (conc_task_id))") # new db for concluded tasks
