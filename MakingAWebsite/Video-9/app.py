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
from supabase import create_client, Client


# pip install flask-login

app = Flask(__name__)
app.secret_key = "supersecretkey"
login_manager = LoginManager()
login_manager.init_app(app)


# Anon Key
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5Z2F1d2ZleHp5cGxnaXd0bG1yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkwMjE2MzcsImV4cCI6MjAzNDU5NzYzN30.UvKsKvyvRz23ZjmY99jFHl9A5MXevQhiRyi1_etcC68"
url = "https://eygauwfexzyplgiwtlmr.supabase.co"
supabase: Client = create_client(url, key)


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    print(response)
    if len(response.data) == 0:
        return None
    user = response.data[0]
    if user:
        return User(user["id"], user["username"], user["password"])
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
                supabase.table("users").insert(
                    {"username": username, "password": hashed_password}
                ).execute()
                flash("Registration successful!")
                return redirect(url_for("home"))
            except Exception as e:
                print("Failed to register a user.")
                print(e)
                flash("Username already exists")
    return render_template_for_user("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        response = (
            supabase.table("users").select("*").eq("username", username).execute()
        )
        user = response.data[0]
        if user and pbkdf2_sha256.verify(password, user["password"]):
            user_obj = User(user["id"], user["username"], user["password"])
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
    if len(content.strip()) == 0:
        flash("Content cannot be empty")
        return redirect(url_for("dashboard"))
    supabase.table("data").insert(
        {"user_id": current_user.id, "content": content}
    ).execute()
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
    response = (
        supabase.table("data").select("*").eq("user_id", current_user.id).execute()
    )
    user_data = response.data
    return render_template_for_user("dashboard.html", user_data=user_data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))  # Actually calls the "home" function.


if __name__ == "__main__":
    app.run(debug=True)
