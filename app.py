import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def main():
    return render_template("main.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        names = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Check that username isn't blank
        if not username or not password:
            return apology("must provide username or password")

        # Check there is no same name in database
        if len(names) == 1:
            return apology(username + " is already existed")


        # Check the two passwords are same
        if password != request.form.get("confirmation"):
            return apology("Put the same password!")

        # generate the hash password to insert
        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Inserting to the DataBase
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pwhash)

        return redirect("/")

    else:
        return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password was submitted
        if not username:
            return render_template("login.html", d=0, password=password)

        if not password:
            return render_template("login.html", d=1, username=username)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", i=0)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


