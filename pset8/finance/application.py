import os
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, avaliable_symbol

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

"""
def avaliable_symbol():
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud.iexapis.com/beta/ref-data/iex/symbols?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        symbol_list = []
        for i in range(len(quote)):
            symbol_list.append(quote[i]["symbol"])
        return symbol_list
    except (KeyError, TypeError, ValueError):
        return None
"""


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    db.execute("CREATE TABLE IF NOT EXISTS portfolio(id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, name TEXT NOT NULL, shares INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")
    db.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, shares TEXT NOT NULL, price INTERGER NOT NULL, datetime TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")
    portfolio = db.execute("SELECT * FROM main.portfolio WHERE user_id = :user_id", user_id=session["user_id"])

    cash = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
    total = (cash[0]["cash"])

    for row in portfolio:
        stock_info = lookup(row["symbol"])
        total = total + (float(stock_info["price"]) * int(row["shares"]))
        row["price"] = usd(stock_info["price"])
        row["total"] = usd((float(stock_info["price"]) * int(row["shares"])))

    return render_template("home.html", portfolio=portfolio, cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if lookup(request.form.get("symbol")) == None:
            return apology("Invalid Symbol")

        try:
            if int(request.form.get("shares")) <= 0:
                return apology("Please purchase a postive integer of shares")
        except ValueError:
            return apology("Please purchase a postive integer of shares")

        stock_info = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        if (rows[0]["cash"]) < (float(stock_info["price"])*int(shares)):
            return apology("Not enough funds in account to complete transaction")

        portfolio = db.execute("SELECT * FROM main.portfolio WHERE user_id = :user_id", user_id=session["user_id"])

        # checks if the symbol the user is trying buy is already in their portfolio
        if any(d["symbol"] == stock_info["symbol"] for d in portfolio):
            for users_symbols in portfolio:
                if users_symbols["symbol"] == stock_info["symbol"]:
                    new_quantity = int(users_symbols["shares"]) + int(shares)
                    db.execute("UPDATE main.portfolio SET shares = :new_quantity WHERE user_id = :user_id and symbol = :symbol",
                        new_quantity=new_quantity, user_id=session["user_id"], symbol=stock_info["symbol"])
                    break
        else:
            db.execute("INSERT INTO main.portfolio (symbol, name, shares,user_id) VALUES(?, ?, ?, ?)",
                stock_info["symbol"], stock_info["name"], int(shares), session["user_id"])

        new_balance = rows[0]["cash"] - (float(stock_info["price"])*int(shares))
        db.execute("UPDATE main.users SET cash = :new_balance WHERE id = :id", new_balance=new_balance, id=session["user_id"])
        db.execute("INSERT INTO main.history (symbol, shares, price, datetime, user_id) VALUES(?, ?, ?, ?, ?)",
            stock_info["symbol"], '+'+str(shares), stock_info["price"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  session["user_id"])

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM main.history WHERE user_id = :user_id",  user_id=session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))

        if symbol == None:
            return apology("Please enter a valid symbol and try again")

        quote_string = (f"A share of {symbol['name']} ({symbol['symbol']}) costs {usd(symbol['price'])}")
        return render_template("quoted.html", symbol_info=quote_string)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must fill all fields", 400)

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username was submitted
        if len(rows) == 1:
            return apology("User already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password") and request.form.get("confirmation"):
            return apology("must provide a password and confirmation", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords did not match", 400)

        pword = request.form.get("password")
        hash = generate_password_hash(pword)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    portfolio = db.execute("SELECT * FROM main.portfolio WHERE user_id = :user_id", user_id=session["user_id"])

    if request.method == "POST":

        try:
            if int(request.form.get("shares")) <= 0:
                return apology("Please sell a postive integer of shares")
        except ValueError:
            return apology("Please sell a postive integer of shares")

        stock_info = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        # checks if user owns any of the stock they are trying to sell
        if not any(x["symbol"] == request.form.get("symbol") for x in portfolio):
            return apology("You do not own any of this stock")

        for row in portfolio:
            if row["symbol"] == request.form.get("symbol"):
                if int(shares) > int(row["shares"]):
                    return apology("You cannot sell more shares than you currently hold")
                elif int(shares) == int(row["shares"]):
                    db.execute("DELETE FROM main.portfolio WHERE user_id = :user_id and symbol = :symbol",
                        symbol=row["symbol"], user_id=session["user_id"])
                else:
                    new_quantity = int(row["shares"]) - int(shares)
                    db.execute("UPDATE main.portfolio SET shares = :new_quantity WHERE user_id = :user_id and symbol = :symbol",
                        new_quantity=new_quantity, user_id=session["user_id"], symbol=row["symbol"])

        user_info = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        new_balance = user_info[0]["cash"] + (float(stock_info["price"])*int(shares))
        db.execute("UPDATE main.users SET cash = :new_balance WHERE id = :id", new_balance=new_balance, id=session["user_id"])
        db.execute("INSERT INTO main.history (symbol, shares, price, datetime, user_id) VALUES(?, ?, ?, ?, ?)",
            stock_info["symbol"], '-'+str(shares), stock_info["price"], datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  session["user_id"])

        return redirect("/")

    return render_template("sell.html", portfolio=portfolio)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
