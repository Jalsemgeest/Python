from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# HTML form template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>Form</title>
</head>
<body>
  <a href="/search">Search</a>
  <form method="POST">
    Name: <input type="text" name="name"><br>
    Age: <input type="text" name="age"><br>
    <input type="submit" value="Submit">
  </form>
</body>
</html>
"""

SEARCH_FORM = """
<!DOCTYPE html>
<html>
<head>
<title>Search Users</title>
</head>
<body>
    <a href="/">Home</a>
    <form method="POST">
        Search for a user: <input type="text" name="search_query"><br>
        <input type="submit" value="Search">
    </form>
    {% if search_results %}
        <h2>Search Results:</h2>
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Age</th>
            </tr>
            {% for user in search_results %}
            <tr>
                <td>{{ user[0] }}</td>
                <td>{{ user[1] }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""


# Initialize the database
def init_db():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def form():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        # Insert into database
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()

    # Query the number of users
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    conn.close()

    message = f'There are currently {user_count} users in the database.'

    return render_template_string(HTML_FORM + message)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_results = []
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Search in the database
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + search_query + '%',))
        search_results = cursor.fetchall()
        conn.close()

    return render_template_string(SEARCH_FORM, search_results=search_results)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
