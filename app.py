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
@app.route("/add_task")
def add_task():
    # Generates <option> instance for category in collection
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_task.html", categories=categories)


# Tells app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
