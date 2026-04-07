import sqlite3
import os

# Get absolute path to database
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'instance', 'users.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Make prudence an admin
cursor.execute('UPDATE users SET is_admin = 1 WHERE username = ?', ('prudence',))
conn.commit()

print("User 'prudence' is now an ADMIN!")
print("\nLogout and login again to see the Admin Panel link.")

conn.close()
