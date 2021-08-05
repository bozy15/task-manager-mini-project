import os
from flask import Flask, flash, render_template, request, session, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

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


# tells app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
