import oracledb
import os
import shutil
from config import ORACLE_CONFIG, UPLOAD_FOLDER

def reset_searchx():
    print("🧹 Starting SEARCHX Fresh Reset...")
    
    # 1. Clear Database Tables
    try:
        conn = oracledb.connect(
            user=ORACLE_CONFIG['user'],
            password=ORACLE_CONFIG['password'],
            dsn=ORACLE_CONFIG['dsn']
        )
        cursor = conn.cursor()
        
        # Disable constraints or delete in order
        tables = [
            "SEARCH_LOGS",
            "INVERTED_INDEX",
            "DOCUMENT_STATS",
            "KEYWORDS",
            "DOCUMENTS"
        ]
        
        for table in tables:
            try:
                print(f"🗑️ Clearing table: {table}...")
                cursor.execute(f"DELETE FROM {table}")
            except Exception as te:
                print(f"⚠️ Warning: Could not clear {table}: {te}")
        
        conn.commit()
        print("✅ Database tables cleared successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")

    # 2. Clear Uploads Folder
    if os.path.exists(UPLOAD_FOLDER):
        print(f"📂 Purging files in {UPLOAD_FOLDER}...")
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ Failed to delete {file_path}. Reason: {e}")
        print("✅ Uploads folder purged.")
    else:
        os.makedirs(UPLOAD_FOLDER)
        print("📁 Created fresh uploads directory.")

    print("\n✨ SEARCHX Reset Complete! Run 'python app.py' to start fresh.")

if __name__ == "__main__":
    reset_searchx()
