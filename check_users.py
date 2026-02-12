import sqlite3

conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

print("=" * 60)
print("ALL USERS IN THE SYSTEM")
print("=" * 60)

users = cursor.execute('SELECT id, username, email, is_admin FROM users').fetchall()

for user in users:
    admin_status = "ADMIN" if user[3] == 1 else "Regular User"
    print(f"ID: {user[0]} | Username: {user[1]} | Email: {user[2]} | Role: {admin_status}")

conn.close()

print("=" * 60)
print("\nTo see Admin Panel:")
print("1. Logout from current account")
print("2. Login with username: admin")
print("3. Password: admin123")
print("4. Look for RED 'Admin Panel' link in navigation")
print("=" * 60)
