import sqlite3

## Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
## Create a sample table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')
## Insert sample data
cursor.executemany('''
INSERT INTO users (name, age) VALUES (?, ?)
''', [('Alice', 30), ('Bob', 25), ('Charlie', 35)])
## Commit
conn.commit()
## Function to execute a query and fetch results
def execute_query(query):
    cursor.execute(query)
    return cursor.fetchall()
## Close the connection when done
def close_connection():
    conn.close()    

if __name__ == "__main__":
    # Example usage
    results = execute_query('SELECT * FROM users')
    for row in results:
        print(row)
    close_connection()