from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        return redirect(url_for("home"))
    return render_template("register.html", header_name="Subscribe!")


if __name__ == "__main__":
    app.run(debug=True)
