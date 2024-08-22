from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re
from passlib.hash import pbkdf2_sha256
from flask_login import (
    LoginManager,
    UserMixin,
    AnonymousUserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# pip install flask-login

app = Flask(__name__)
app.secret_key = "supersecretkey"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2])
    return None


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
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    print("Rendering home")
    return render_template_for_user("index.html")
    # return "Welcome to the Home Page"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not re.match(r"^[a-zA-Z0-9]+$", username):
            flash("Username must contain only letters and numbers")
        elif len(password) < 6:
            flash("Password must be at least 6 characters long")
        else:
            hashed_password = pbkdf2_sha256.hash(password)
            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password),
                )
                conn.commit()
                conn.close()
                flash("Registration successful!")
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Username already exists")
    return render_template_for_user("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and pbkdf2_sha256.verify(password, user[2]):
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
    return render_template_for_user("login.html")


@app.route("/add_data", methods=["POST"])
@login_required
def add_data():
    content = request.form["content"]
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO data (user_id, content) VALUES (?, ?)", (current_user.id, content)
    )
    conn.commit()
    conn.close()
    flash("Data added successfully!")
    return redirect(url_for("dashboard"))


def render_template_for_user(template, user_data=None):
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return render_template(template, user=current_user, user_data=user_data)
    return render_template(template)


@app.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM data WHERE user_id = ?", (current_user.id,))
    user_data = cursor.fetchall()
    conn.close()
    return render_template_for_user("dashboard.html", user_data=user_data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))  # Actually calls the "home" function.


if __name__ == "__main__":
    app.run(debug=True)
