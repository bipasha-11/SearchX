import os
import sys

# Ensure backend folder is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import get_connection

def delete_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        print(f"Attempting to delete user with email: {email}")
        
        # We also need to get user_id to set documents owner_id to NULL if needed, 
        # or delete their documents. Usually setting owner_id to NULL is safer or deleting.
        # Let's see if we have them.
        cursor.execute("SELECT user_id FROM USERS WHERE lower(email) = lower(:1)", (email,))
        row = cursor.fetchone()
        
        if row:
            user_id = row[0]
            print(f"Found user_id: {user_id}. Nullifying owner_id on their documents...")
            try:
                cursor.execute("UPDATE DOCUMENTS SET owner_id = NULL WHERE owner_id = :1", (user_id,))
            except Exception as e:
                print(f"Ignoring document update error: {e}")
                
            cursor.execute("DELETE FROM USERS WHERE lower(email) = lower(:1)", (email,))
            print("User deleted from USERS table.")
        else:
            print("User not found in USERS table.")
            
        cursor.execute("DELETE FROM PENDING_USERS WHERE lower(email) = lower(:1)", (email,))
        print("User deleted from PENDING_USERS table.")
        
        conn.commit()
        print("Commit completed successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    delete_user('vabipasha@gmail.com')
