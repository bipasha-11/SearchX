"""
SEARCHX - Database Connection Manager
PostgreSQL compatible using psycopg2
"""

import os
import psycopg2
from psycopg2 import extras

def get_connection():
    """
    Create and return a PostgreSQL database connection.
    Uses DATABASE_URL environment variable (from Neon/Render).
    """
    try:
        # Fallback for local development if needed, but primary is DATABASE_URL
        db_url = os.environ.get('DATABASE_URL')
        
        if not db_url:
            # You can put a default local postgres string here if you have one
            print("[SEARCHX] Warning: DATABASE_URL not set!")
            
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"[SEARCHX] Database connection error: {e}")
        raise

def test_connection():
    """Test if database is reachable."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'SEARCHX_OK'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] == 'SEARCHX_OK'
    except Exception as e:
        print(f"[SEARCHX] Connection test failed: {e}")
        return False
