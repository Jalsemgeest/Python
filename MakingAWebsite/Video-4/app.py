from flask import Flask, render_template, request, redirect, url_for, flash
import re
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")
    # return "Welcome to the Home Page"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        if not re.match(r"^[a-zA-Z0-9]+$", username):
            flash("Username must contain only letters and numbers")
        elif len(password) < 6:
            flash("Password must be at least 6 characters long")
        else:
            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password),
                )
                conn.commit()
                conn.close()
                flash("Registration successful!")
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Username already exists")
    return render_template("register.html", header_name="Subscribe")


if __name__ == "__main__":
    app.run(debug=True)
