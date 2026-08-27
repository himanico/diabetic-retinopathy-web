import sqlite3
import os

db_path = os.path.join("instance", "database.db")

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE screening_result
        ADD COLUMN created_at DATETIME
    """)

    print("created_at column added successfully.")

except sqlite3.OperationalError as e:

    if "duplicate column name" in str(e).lower():
        print("created_at column already exists.")

    else:
        print("Error:", e)

conn.commit()
conn.close()

print("Database update completed.")