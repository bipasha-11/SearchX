from db import get_connection
import bcrypt

def create_demo():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT COUNT(*) FROM USERS WHERE username = 'demo_user'")
        if cursor.fetchone()[0] == 0:
            pw = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("""
                INSERT INTO USERS (username, email, password_hash, full_name)
                VALUES (:u, :e, :p, :f)
            """, {'u': 'demo_user', 'e': 'demo@searchx.com', 'p': pw, 'f': 'Demo User'})
            print("Demo user created.")
        else:
            print("Demo user already exists.")
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_demo()
