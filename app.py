import os
from flask import Flask

# imports env if a path to "env.py" is found
if os.path.exists("env.py"):
    import env

# Creates an instance of the Flask class
app = Flask(__name__)


# test function for proof of concept
@app.route("/")
def hello():
    return "Hello World!"


# tells app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
