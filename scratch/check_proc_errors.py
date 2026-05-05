import oracledb
from db import get_connection

def check_errors():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Checking compilation errors for PROC_ADD_DOCUMENT...")
    cursor.execute("""
        SELECT line, position, text 
        FROM user_errors 
        WHERE name = 'PROC_ADD_DOCUMENT' 
        ORDER BY line, position
    """)
    errors = cursor.fetchall()
    if not errors:
        print("No errors found in USER_ERRORS. Checking status...")
        cursor.execute("SELECT status FROM user_objects WHERE object_name = 'PROC_ADD_DOCUMENT'")
        row = cursor.fetchone()
        print(f"Status: {row[0] if row else 'NOT FOUND'}")
    else:
        for line, pos, text in errors:
            print(f"Line {line}, Pos {pos}: {text}")
            
    cursor.close()
    conn.close()

if __name__ == "__main__":
    import os
    import sys
    sys.path.append('d:/SEARCHX/backend')
    check_errors()
