import oracledb
import os
from db import get_connection

def run_sql_file(filename):
    print(f"Running {filename}...")
    conn = get_connection()
    cursor = conn.cursor()
    
    with open(filename, 'r') as f:
        sql = f.read()
    
    # Oracle scripts often have '/' as delimiter for blocks
    parts = sql.split('/')
    for part in parts:
        stmt = part.strip()
        if not stmt:
            continue
        try:
            # Remove trailing semicolon only for simple statements, not for PL/SQL blocks
            stmt_lower = stmt.lower()
            is_block = stmt_lower.startswith('begin') or \
                       stmt_lower.startswith('declare') or \
                       stmt_lower.startswith('create or replace') or \
                       stmt_lower.startswith('--') or \
                       'procedure' in stmt_lower or \
                       'trigger' in stmt_lower
            
            if stmt.endswith(';') and not is_block:
                stmt = stmt[:-1]
            
            cursor.execute(stmt)
            print("  Executed statement.")
        except Exception as e:
            print(f"  Error: {e}")
            # Continue for "column already exists" errors if they happen despite the check
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    run_sql_file('d:/SEARCHX/database/add_file_storage.sql')
