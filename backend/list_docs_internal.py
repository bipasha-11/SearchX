from db import get_connection
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT doc_id, title, file_name FROM DOCUMENTS")
results = cursor.fetchall()
if not results:
    print("No documents found in database.")
for row in results:
    print(f"ID: {row[0]} | Title: {row[1]} | File: {row[2]}")
cursor.close()
conn.close()
