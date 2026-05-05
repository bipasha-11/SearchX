
import os
import psycopg2
from psycopg2 import extras
import bcrypt
import datetime
import random
from config import SMTP_CONFIG, AI_CONFIG
import google.generativeai as genai
from nltk.stem import PorterStemmer
import nltk

# Initialize Gemini
genai.configure(api_key=AI_CONFIG['GEMINI_API_KEY'])
ai_model = genai.GenerativeModel(AI_CONFIG['MODEL_NAME'])
stemmer = PorterStemmer()

def get_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        # Fallback to hardcoded for this one-time injection if env is missing locally
        db_url = "postgresql://neondb_owner:npg_R2dIit6YpLNo@ep-empty-water-a17p6665-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    return psycopg2.connect(db_url)

def generate_summary(text, title):
    try:
        sample = text[:5000]
        prompt = f"Summarize this legal document titled '{title}' in 3 professional sentences.\n\n{sample}"
        response = ai_model.generate_content(prompt)
        return response.text.strip()
    except:
        return f"Legal summary for {title} indexed for retrieval."

def inject():
    print("🚀 Starting Demo Data Injection for Bipasha11...")
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Ensure User Exists
        cursor.execute("SELECT user_id FROM USERS WHERE username = 'Bipasha11'")
        res = cursor.fetchone()
        if not res:
            print("❌ User Bipasha11 not found! Please register first.")
            return
        user_id = res[0]
        print(f"✅ Found Bipasha11 (ID: {user_id})")

        # 2. Get Test Cases
        test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'TEST_CASES')
        files = [f for f in os.listdir(test_dir) if f.endswith('.txt')]
        
        for fname in files:
            print(f"📄 Processing {fname}...")
            fpath = os.path.join(test_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title = fname.replace('.txt', '').replace('_', ' ').title()
            summary = generate_summary(content, title)
            
            # Insert Doc
            cursor.execute("""
                INSERT INTO DOCUMENTS (title, file_name, content_length, file_type_id, language_id, category, jurisdiction, summary, file_data, owner_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING doc_id
            """, (title, fname, len(content), 3, 1, 'Case Summary', 'Supreme Court', summary, content.encode('utf-8'), user_id))
            doc_id = cursor.fetchone()[0]
            
            # Indexing
            words = content.lower().split()
            freq = {}
            for w in words:
                if len(w) > 2:
                    stemmed = stemmer.stem(w)
                    freq[stemmed] = freq.get(stemmed, 0) + 1
            
            for word, f in freq.items():
                if len(word) <= 50:
                    cursor.execute("INSERT INTO INVERTED_INDEX (word, doc_id, frequency) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (word, doc_id, f))
            
            print(f"   ✅ Indexed {len(freq)} terms.")
        
        conn.commit()
        print("\n✨ SUCCESS! All demo cases are now in Bipasha11's account.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ FAILED: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    inject()
