import sqlite3

conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Make prudence an admin
cursor.execute('UPDATE users SET is_admin = 1 WHERE username = ?', ('prudence',))
conn.commit()

print("User 'prudence' is now an ADMIN!")
print("\nLogout and login again to see the Admin Panel link.")

conn.close()
