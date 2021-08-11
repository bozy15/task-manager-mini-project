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


# Route for resgistering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # chesks if username is already in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        # if username is already in the database, return an error
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # if username is not in the database, register the user
        register = (
            {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password")),
            }
        )
        mongo.db.users.insert_one(register)

        # Put the new user into A "session" cookie 
        # so that the user can be logged in
        # (this is a security measure)
        session["user"] = request.form.get("username").lower()
        flash("User successfully registered")

    return render_template("register.html")


# tells app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
