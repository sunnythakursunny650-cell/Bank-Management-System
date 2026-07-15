import sqlite3

# Database Connection
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    account_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    balance REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Database Created Successfully ✅")