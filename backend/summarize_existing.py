import os
import google.generativeai as genai
from db import get_connection
from config import AI_CONFIG, UPLOAD_FOLDER

# Configure Gemini
genai.configure(api_key=AI_CONFIG['GEMINI_API_KEY'])
model = genai.GenerativeModel(AI_CONFIG['MODEL_NAME'])

def extract_text_simple(filename):
    """Simple text extractor helper for migration."""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return None
    
    # Try reading as plain text first
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read(10000) # Get first 10k chars
    except:
        return None

def generate_summary(text):
    if not text or len(text) < 20:
        return "Not enough content to summarize."
    
    try:
        prompt = (
            "You are a professional legal assistant. Provide a concise 3-sentence executive summary "
            "of the following legal document content. Focus on core purpose and obligations.\n\n"
            f"TEXT: {text[:5000]}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing: {e}")
        return None

def migrate_summaries():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Fetching documents without summaries...")
    cursor.execute("SELECT doc_id, file_name, title FROM DOCUMENTS WHERE summary IS NULL")
    docs = cursor.fetchall()
    
    print(f"Found {len(docs)} documents to summarize.")
    
    for doc_id, file_name, title in docs:
        print(f"Processing: {title} ({file_name})...")
        text = extract_text_simple(file_name)
        
        if text:
            summary = generate_summary(text)
            if summary:
                cursor.execute(
                    "UPDATE DOCUMENTS SET summary = :sum WHERE doc_id = :id",
                    {'sum': summary, 'id': doc_id}
                )
                conn.commit()
                print(f"Success! Summary added for {title}")
            else:
                print(f"Failed to generate summary for {title}")
        else:
            print(f"Skipping {title}: Physical file not found or unreadable.")

    cursor.close()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate_summaries()
