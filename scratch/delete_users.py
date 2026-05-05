import sys
import os

# Add backend to path so we can import app
sys.path.append(r'd:\SEARCHX\backend')

from app import app, get_connection

def delete_users():
    with app.app_context():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM PENDING_USERS WHERE email IN ('bipashavijayanad@gmail.com', 'vabipasha@gmail.com')")
            print(f"Deleted {cursor.rowcount} users from PENDING_USERS.")
            
            cursor.execute("DELETE FROM USERS WHERE email IN ('bipashavijayanad@gmail.com', 'vabipasha@gmail.com')")
            print(f"Deleted {cursor.rowcount} users from USERS.")
            
            conn.commit()
            print("Commit successful.")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    delete_users()
