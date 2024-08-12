"""
This is a simple Flask app that demonstrates how to use Flask, Jinja2 templating, and a mini data-store

To run this app, after installing Flask, run either:
    FLASK_APP=app FLASK_DEBUG=True flask run
or (invoking the script directly):
    python app.py

You can then access the app from your browser at localhost:8080
By having FLASK_DEBUG=True, Flask will automatically reload the app when change the code
Just note that it reset the data-store each time you restart the app

To run in production, we'll use gunicorn, via:
    gunicorn app:app
"""
from flask import Flask, render_template, request, redirect, url_for

# Our Flask app object
app = Flask(__name__)

# A mini data-store for our tasks, using a basic list of strings
taskDatastore = []


@app.route("/")
def index():
    """Render the home page"""
    return render_template("index.html")


@app.route("/tasks")
def task_list():
    """Render the tasks page, using our mini data-store"""
    return render_template("tasks.html", tasks=taskDatastore)


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task to our mini data-store"""
    new_task = request.form.get("task")
    taskDatastore.append(new_task)
    return redirect(url_for("task_list"))


# TODO: Change this to use a DELETE request
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Delete a task from our mini data-store based on its id"""
    taskDatastore.pop(task_id)
    return redirect(url_for("task_list"))


if __name__ == "__main__":
    app.run(debug=True, port=8080)