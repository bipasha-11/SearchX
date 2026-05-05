import os
import google.generativeai as genai
from db import get_connection
from config import AI_CONFIG, UPLOAD_FOLDER

genai.configure(api_key=AI_CONFIG['GEMINI_API_KEY'])
model = genai.GenerativeModel(AI_CONFIG['MODEL_NAME'])

def run_fix():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doc_id, file_name, title FROM DOCUMENTS")
    docs = cursor.fetchall()
    
    for doc_id, file_name, title in docs:
        print(f"Fixing {title}...")
        filepath = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.exists(filepath):
             # Just use title + some constant if it's too hard to read for this quick fix
             # Or try to read it
             try:
                 with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                     content = f.read(5000)
             except:
                 content = f"Legal document titled {title}"
             
             prompt = f"Summarize this legal document titled '{title}' in exactly 3 short sentences. Focus on the core purpose and key obligations. Maintain a formal tone.\n\nTEXT:\n{content[:5000]}"
             try:
                 # Safety settings
                 safety_settings = [
                     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                 ]
                 res = model.generate_content(prompt, safety_settings=safety_settings)
                 
                 if hasattr(res, 'candidates') and res.candidates and res.candidates[0].content.parts:
                     summary = res.text.strip()
                 else:
                     summary = f"Executive summary for '{title}' was restricted by safety filters. The document core is indexed."
                 
                 cursor.execute("UPDATE DOCUMENTS SET summary = :s WHERE doc_id = :id", {'s': summary, 'id': doc_id})
                 print(f"Updated: {title}")
             except Exception as e:
                 print(f"Failed {title}: {e}")
        else:
            print(f"File missing: {filepath}")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_fix()
