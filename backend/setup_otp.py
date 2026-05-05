from db import get_connection
import oracledb

def setup_otp_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Drop table if exists
    try:
        cursor.execute("DROP TABLE PENDING_USERS CASCADE CONSTRAINTS")
    except:
        pass
        
    # Create table
    cursor.execute("""
        CREATE TABLE PENDING_USERS (
            email         VARCHAR2(255) PRIMARY KEY,
            username      VARCHAR2(100),
            password_hash VARCHAR2(500),
            full_name     VARCHAR2(200),
            otp           VARCHAR2(10),
            otp_expiry    DATE,
            created_at    DATE DEFAULT SYSDATE
        )
    """)
    
    conn.commit()
    print("PENDING_USERS table created successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_otp_table()
