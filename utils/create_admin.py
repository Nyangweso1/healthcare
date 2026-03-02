"""
Create Admin User Script
Run this to create an admin account for the Healthcare Prediction System
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_admin():
    print("=" * 60)
    print("CREATE ADMIN USER - Healthcare Prediction System")
    print("=" * 60)
    print()
    
    # Get admin details
    username = input("Enter admin username: ").strip()
    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    
    # Validation
    if not username or not email or not password:
        print("❌ All fields are required!")
        return
    
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters!")
        return
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Connect to database
    try:
        conn = sqlite3.connect('instance/users.db')
        cursor = conn.cursor()
        
        # Check if username exists
        existing = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            print(f"❌ Username '{username}' already exists!")
            
            # Ask if want to make existing user admin
            choice = input(f"Make existing user '{username}' an admin? (yes/no): ").strip().lower()
            if choice == 'yes':
                cursor.execute('UPDATE users SET is_admin = 1 WHERE username = ?', (username,))
                conn.commit()
                print(f"✅ User '{username}' is now an admin!")
            conn.close()
            return
        
        # Insert admin user
        cursor.execute('''
            INSERT INTO users (username, email, password, is_admin)
            VALUES (?, ?, ?, 1)
        ''', (username, email, hashed_password))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        print()
        print("=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"User ID: {user_id}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Role: Administrator")
        print()
        print("You can now log in with these credentials at /login")
        print("Access admin panel at /admin after logging in")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")


if __name__ == "__main__":
    create_admin()
