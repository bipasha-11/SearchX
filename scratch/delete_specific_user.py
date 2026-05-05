import sys
import os

sys.path.append(r'd:\SEARCHX\backend')

from app import app, get_connection

def delete_user():
    with app.app_context():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1. Get user_id for Bipasha11
            cursor.execute("SELECT user_id FROM USERS WHERE username = 'Bipasha11' OR email LIKE 'bipasha.v2024%'")
            user_rows = cursor.fetchall()
            
            for (uid,) in user_rows:
                print(f"Processing user_id: {uid}")
                
                # Delete search logs
                try: cursor.execute("DELETE FROM SEARCH_LOGS WHERE user_id = :u_id", {'u_id': uid})
                except Exception as e: print(f"Skip SEARCH_LOGS: {e}")
                
                # Find all documents owned by this user
                try:
                    cursor.execute("SELECT doc_id FROM DOCUMENTS WHERE owner_id = :u_id", {'u_id': uid})
                    doc_rows = cursor.fetchall()
                    
                    for (doc_id,) in doc_rows:
                        try: cursor.execute("DELETE FROM INVERTED_INDEX WHERE doc_id = :did", {'did': doc_id})
                        except Exception as e: pass
                        try: cursor.execute("DELETE FROM DOCUMENT_STATS WHERE doc_id = :did", {'did': doc_id})
                        except Exception as e: pass
                    
                    cursor.execute("DELETE FROM DOCUMENTS WHERE owner_id = :u_id", {'u_id': uid})
                except Exception as e: print(f"Skip DOCUMENTS: {e}")
                
                try: cursor.execute("DELETE FROM USERS WHERE user_id = :u_id", {'u_id': uid})
                except Exception as e: print(f"Skip USERS: {e}")
                print(f"Deleted user_id {uid} completely.")
                
            cursor.execute("DELETE FROM PENDING_USERS WHERE username = 'Bipasha11' OR email LIKE 'bipasha.v2024%'")
            print(f"Deleted {cursor.rowcount} from PENDING_USERS.")
            
            conn.commit()
            print("Commit successful.")
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    delete_user()
