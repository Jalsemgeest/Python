# pip install db-sqlite3

import sqlite3

# Connect to a database (creates a new one if not exists)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor() 

# Define a table schema and create the table
cursor.execute('''
   CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      age INTEGER
   )
''')

# Insert data into the 'users' table
# cursor.execute('''
#    INSERT INTO users (name, age) VALUES
#       ('John Doe', 25),
#       ('Jane Smith', 30),
#       ('Bob Johnson', 22)
# ''')

# # Execute a SELECT query
cursor.execute('SELECT * FROM users')

# Fetch all rows and print them
rows = cursor.fetchall()
for row in rows:
   print(row) 

# Commit the changes and close the connection
conn.commit()
conn.close()




# Transactional
cursor.executescript('''
  BEGIN;
  # read
  # modify
  # write
  COMMIT;
''')

# 1. Read the balance of account “A”.
# 2. Read the balance of account “B”.
# 3. Reduce the balance of account “A”.
# --- 
# 4. Add the balance to account “B”.
