import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tkinter import messagebox

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproject.db")

@app.route("/recipe_index")
@login_required
def recipe_index():
    """Show portfolio of stocks"""
    title = db.execute("SELECT title FROM menus WHERE user_id = ?", session["user_id"])
    if not title:
        return render_template("recipe_index.html")

    return render_template("recipe_index.html", titles=title)

@app.route("/recipe_register", methods=["GET", "POST"])
@login_required
def recipe_register():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure password was submitted
        title = request.form.get("title")
        if not title:
            return apology("タイトルを入力してください")

        titles = db.execute("SELECT title FROM menus WHERE user_id = ?", session['user_id'])
        if(title in [tl.get('title') for tl in titles]):
            return apology("同じ料理名のメニューがあります")

        number = int(request.form.get("number"))
        if not number:
            return apology("何人前なのか入力してください")

        if number <= 0:
            return apology("正の整数で人数を入力してください")

        stuff = ""
        stuffs = ""

        for food, quantity in zip(request.form.getlist("stuffs"), request.form.getlist("quantitys")):
            if ((not food) | (not quantity)):
                return apology("食材と分量を適切に入力してください")
            stuff = food + " " + quantity + "/"
            stuffs = stuffs + stuff

        fl = ""
        for flows in zip(request.form.getlist("flows")):
            if not flows:
                return apology("手順を適切に入力してください")

            fl = fl + flows[0] + "/  /"

        db.execute("INSERT INTO menus (user_id, title, stuff, flow, number) VALUES(?, ?, ?, ?, ?)", session['user_id'], title, stuffs, fl, number)

        flash("Registered!", "success")

        # Redirect user to home page
        return redirect("/recipe_index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("recipe_register.html")



@app.route("/detail/<string:title>")
@login_required
def detail_menu(title):
    menu = db.execute("SELECT * FROM menus WHERE user_id = ? AND title = ?", session['user_id'], title)
    s = menu[0]['stuff'].split('/')
    stuffquantity = []
    for food in s:
        if food != '':
            foods = food.split(' ')
            stuff_temp = {}
            stuff_temp['stuff'] = foods[0]
            stuff_temp['quantity'] = foods[1]
            stuffquantity.append(stuff_temp)


    fl = menu[0]['flow'].split("/  /")
    fl.pop()
    return render_template("detail.html", menu = menu, foods = stuffquantity, flows = fl)

@app.route("/detail", methods=["GET", "POST"])
@login_required
def detail():
    title = request.form.get("menu")
    menu = db.execute("SELECT * FROM menus WHERE user_id = ? AND title = ?", session['user_id'], title)
    s = menu[0]['stuff'].split('/')
    stuffquantity = []
    #stuff_temp = {}
    for food in s:
        if food != '':
            foods = food.split(' ')
            stuff_temp = {}
            stuff_temp['stuff'] = foods[0]
            stuff_temp['quantity'] = foods[1]
            stuffquantity.append(stuff_temp)

    fl = menu[0]['flow'].split("/  /")
    fl.pop()
    return render_template("detail.html", menu = menu, foods = stuffquantity, flows = fl)


@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure password was submitted
        old_password = request.form.get("oldpassword")
        if not old_password:
            return apology("パスワードを入力してください")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_password):
            return apology("パスワードを確認してください")

        new_password = request.form.get("newpassword1")
        confirm_password = request.form.get("newpassword2")

        if (new_password != confirm_password):
            return apology("新しいパスワードが一致している確認して下さい")

        hash_password = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash_password, session['user_id'])

        flash("Changed!", "success")

        # Redirect user to home page
        return redirect("/recipe_index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("setting.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("ユーザ名を入力してください")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("パスワードを入力してください")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("ユーザ名かパスワードが間違えています")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/recipe_index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/recipe_index")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        names = db.execute("SELECT username FROM users")

        if(not name):
            return apology("ユーザ名を入力してください")
        if(name in [nm.get('username') for nm in names]):
            return apology("ユーザ名が重複しています")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if((not password) | (password != confirmation)):
            return apology("パスワードが正しいか確認してください")

        hash_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, hash_password)
        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Registered!", "success")
        return redirect("/recipe_index")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
