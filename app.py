import os
from unittest import result

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from flask import jsonify



from helper import login_required, lookup, look, rating

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

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
def main():

    if len(session) != 1:
        return render_template("main.html")

    else:
        return render_template("search-mobile.html")
    


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        # Check that username isn't blank
        if not username  and not password and not confirm:
            return render_template("signup.html",a=0)

        if username:
            if not password:
                if not confirm:
                    return render_template("signup.html",d=0, username=username)
                return render_template("signup.html",d=1, username=username, confirm=confirm)
            
            if not confirm:
                return render_template("signup.html",d=2, username=username, password=password)

        if password:
            if not username:
                if not confirm:
                    return render_template("signup.html",d=3, password=password)
                return render_template("signup.html",d=4, password=password, confirm=confirm)

            if not confirm:
                return render_template("signup.html",d=2, username=username, password=password)
        
        if confirm:
            if not username:
                if not password:
                    return render_template("signup.html",d=5, confirm=confirm)
                return render_template("signup.html",d=4, password=password, confirm=confirm)

            if not password:
                return render_template("signup.html",d=1, username=username, confirm=confirm)
            
        # Check there is no same name in database
        names = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(names) == 1:
            return render_template("signup.html",i=0, password=password, confirm=confirm)

        # Check the two passwords are same
        if password != confirm:
            return render_template("signup.html",i=1, username=username, password=password)

        # generate the hash password to insert
        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Inserting to the DataBase
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, pwhash)

        return redirect("/login")

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
        if not username and not password:
            return render_template("login.html",a=0)

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


@app.route("/search", methods=["GET"])
def search():

    title = request.args.get("title")

    results = lookup(str(title))

    return render_template("result.html", results=results, title=title)

@app.route("/add", methods=["POST"])
def add():

    if request.method == "POST":

        title = request.form.get("title")
        name = request.form.get("name")
        date = request.form.get("date")
        Type = request.form.get("type")
        img = request.form.get("img")

        arr = ["/title/", "/"]

        for a in arr:
            title = title.replace(a, "")

        title = {"name": title}

        rate = rating(title["name"]) 

        own = db.execute("SELECT name FROM p_list WHERE user_id = ?", session["user_id"])

        if title in own:
            return jsonify({'error': 'Admin access is required'}), 401

        else:
            db.execute("INSERT INTO p_list (user_id, name, title, date, type, rating, img) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], name, title["name"], date, Type, rate, img)
            return jsonify({'success': 'good'}), 200
                   
    return redirect("/")


@app.route("/list")
def plist():

    lists = []

    plist = db.execute("SELECT * FROM p_list WHERE user_id = ?", session["user_id"])
        
    return render_template("list.html", lists=plist)