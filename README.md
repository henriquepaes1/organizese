# Organize.se
Organize.se stands for **organize yourself** in English.
## What is it?
#### Description:
A simple web app that helps you organize your tasks in a clean interface. You have the hability to add new tasks, conclude and delete existing tasks easily. Stay tuned to see new coming features
like timestamps and performance graphs.
#### See how organize.se works here: https://youtu.be/8ZLjxwTzk5E

## How was it built?
Organize.se was built using Flask, Python, HTML, CSS and SQL. All skills provided by CS50 :)
With this project, I were able to finally take out some *training wheels* CS50 IDE provided. I needed to use sqlite3 in other environment and my experience with this final
project was much more than coding a website, it was more about **learn how to learn** by looking up for information and apllying it instantly in a functional application.
It was my first experience out of the labs and problem sets of the course, which were, indeed, really challenging and well built by CS50's team. It was more of a real-life experience
that sets the path for my carrer.

## Register
In this screen, you'll need to create an account by providing an username and two matching passwords. Talking about **security**, we used the *Werkzeug* library to hash the password and check the hashing,
so, in the database the passwords are safe.

## Log in
Provide an username, a password and the system will check for your account in the system. Again the *Werkzeug* library comes to play, as it do the job to check the hash saved in yhe database with
the password the user typed.

## See tasks
This is the main screen, where you can see the tasks you added and two possible actions: conclude or delete. You can also create a new task by clicking the "add task" button.
The tasks are returned by the database with function *fetchall*, that access the database via the *cursor*, this is the approach we used to access the local database, using sqlite3,
for more information, check here: https://docs.python.org/3/library/sqlite3.html

## Create task
In this screen you just need to provide a description of your task, by adding a new task to the database, you're automatically redirect to the main screen, where you can see your new task.

## Delete task
This feature doesn't have any screen. You just remove your task from the database. You need to identify that the delete button was clicked, which is done by *request.form*, and which task was clicked,
and this approach is possible via *invisible inputs* in HTML


## Concluded task
In this screen, you can see the tasks you've already concluded. The process to conclude a task, equal to delete, require that you identify that conclude button was clicked and which task was clicked.

## Who am I?
My name is Henrique, I am a computer engineering student at University of Sao Paulo.
If you have any feedback, feel free to contact me:
hpaesdesouza@gmail.com
https://www.linkedin.com/in/henriquepaes1/

## Final considerations
I would like to appreciate all of CS50's staff for the amazing work in this course and extend my acknowledgements to all members of CS50 community that were always really willing to help
me with my struggles during the course.

