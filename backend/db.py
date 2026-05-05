"""
SEARCHX - Database Connection Manager
Oracle 11g compatible using oracledb in thin mode
"""

import oracledb
from config import ORACLE_CONFIG


def get_connection():
    """
    Create and return an Oracle database connection.
    Uses oracledb in thin mode (no Oracle Client needed).
    """
    try:
        conn = oracledb.connect(
            user=ORACLE_CONFIG['user'],
            password=ORACLE_CONFIG['password'],
            dsn=ORACLE_CONFIG['dsn']
        )
        return conn
    except oracledb.Error as e:
        print(f"[SEARCHX] Database connection error: {e}")
        raise


def test_connection():
    """Test if Oracle database is reachable."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'SEARCHX_OK' FROM DUAL")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] == 'SEARCHX_OK'
    except Exception as e:
        print(f"[SEARCHX] Connection test failed: {e}")
        return False
