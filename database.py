import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shreyas",   # Replace with your password
    database="snippets_manager"
)

cursor = connection.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS snippets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    language VARCHAR(100) NOT NULL,
    code TEXT NOT NULL,
    description TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")