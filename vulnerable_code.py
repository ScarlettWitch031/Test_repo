import os
import sqlite3

# Vulnerable: Hardcoded credentials
username = "admin"
password = "password123"

# Vulnerable: SQL Injection
def authenticate_user(user, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        print("Authentication successful!")
    else:
        print("Authentication failed!")

    conn.close()

# Vulnerable: Insecure file handling
def upload_file(file):
    if not file:
        print("No file uploaded!")
        return

    # Vulnerable: Insecure file path
    file_path = f"uploads/{file.filename}"
    
    # Vulnerable: Potential arbitrary file upload
    with open(file_path, 'wb') as f:
        f.write(file.read())

    print(f"File uploaded to {file_path}")

# Example usage of the vulnerabilities
authenticate_user("admin", "password123")

# Vulnerable file upload
class File:
    def __init__(self, filename):
        self.filename = filename

file = File("../../../etc/passwd")  # Simulating a potential attack
upload_file(file)

