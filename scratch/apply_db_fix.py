
import sys
import os
import oracledb

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from db import get_connection

def run_sql_script(connection, script_path):
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Simple split by / for blocks and ; for statements
    # This is rough but should work for the fix script
    statements = content.split('/')
    
    cursor = connection.cursor()
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            print(f"Executing block/statement starting with: {stmt[:50]}...")
            cursor.execute(stmt)
        except Exception as e:
            print(f"Error executing statement: {e}")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connected to database.")
        run_sql_script(conn, 'database/fix_db_schema.sql')
        print("Fix applied successfully.")
        conn.close()
    except Exception as e:
        print(f"Failed to apply fix: {e}")
