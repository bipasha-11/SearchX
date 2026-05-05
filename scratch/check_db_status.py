
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from db import get_connection, test_connection
    import oracledb

    print("Checking database connection...")
    if test_connection():
        print("SUCCESS: Connection to Oracle is OK.")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        tables_to_check = ['USERS', 'DOCUMENTS', 'TERMS', 'INVERTED_INDEX', 'STOPWORDS', 'QUERY_LOG']
        print("\nChecking tables:")
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: EXISTS ({count} rows)")
            except oracledb.Error as e:
                print(f"  {table}: MISSING or ERROR ({e})")
        
        cursor.close()
        conn.close()
    else:
        print("FAILED: Could not connect to Oracle database.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
