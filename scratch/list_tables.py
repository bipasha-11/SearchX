from db import get_connection
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    for row in cursor.fetchall():
        print(row[0])
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
