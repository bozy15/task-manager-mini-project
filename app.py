import os
from flask import Flask, flash, render_template, request, session, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# imports env if a path to "env.py" is found
if os.path.exists("env.py"):
    import env

# Creates an instance of the Flask class
app = Flask(__name__)

# Grabs database name, connection string and Secret key from env.py
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Creates an instance of the PyMongo class
mongo = PyMongo(app)

# test function for proof of concept
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


# Route for registering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checks if username is already in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        # if username is already in the database, return an error
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # if username is not in the database, register the user
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # Put the new user into A "session" cookie
        # so that the user can be logged in
        session["user"] = request.form.get("username").lower()
        flash("User successfully registered")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Route for logging in a user
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Checks if the username is in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        # If the username is in the database, check if the password is correct
        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                # Put the user into a 'session' cookie
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or password")
                return redirect(url_for("login"))
        else:
            # User does not exist
            flash("Incorrect Username and/or password")
            return redirect(url_for("login"))
    return render_template("login.html")


# Route for users profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grabs the session user's username from the database
    username = mongo.db.users.find_one({"username": session["user"]})["username"]

    # if the user is logged in, show their profile
    # otherwise, redirect to login page
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# Route for logging out a user
@app.route("/logout")
def logout():
    # removes the user's session cookie
    session.pop("user", None)
    flash("You have been logged out")
    return redirect(url_for("login"))


# Route for adding a task
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        # Grabs the task details from the form and stores them in a dictionary
        task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        # Grabs the task from the task dictionary and adds it to the database
        mongo.db.tasks.insert_one(task)
        flash("Task Successfully Added")
        # Redirects to the profile page
        return redirect(url_for("get_tasks"))
    # Generates <option> instance for category in collection
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_task.html", categories=categories)


# Route for editing a task
@app.route("/edit_task/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # Grabs the task from the database
    task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        # Grabs the task details from the form and stores them in a dictionary
        submit = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        # Grabs the task from the task dictionary and adds it to the database
        mongo.db.tasks.update({"_id": ObjectId(task_id)}, submit)
        flash("Task Successfully Updated")

    # Grabs the category from the database
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_task.html", task=task, categories=categories)


# Route for deleting a task
@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    mongo.db.tasks.remove({"_id": ObjectId(task_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for("get_tasks"))

# Route for getting categories
@app.route("/get_categories")
def get_categories():
    # Grabs all the categories from the database
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


# Tells app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
