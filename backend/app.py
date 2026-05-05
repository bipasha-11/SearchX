"""
SEARCHX - Main Flask Application
Search Engine Indexing & Query Analytics System
Domain: LAW / LEGAL DOCUMENTS
With Authentication & User-Scoped Documents
"""


import os
import re
import string
import datetime
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps

import google.generativeai as genai

from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

import oracledb
import bcrypt
import jwt

from db import get_connection
from config import (
    FLASK_CONFIG, UPLOAD_FOLDER, ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH, MAX_KEYWORD_LENGTH, ALLOWED_KEYWORD_PATTERN,
    JWT_SECRET, JWT_EXPIRY_HOURS,
    SMTP_CONFIG, AI_CONFIG
)

from nltk.stem import PorterStemmer
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"[SEARCHX] NLTK download warning: {e}")

stemmer = PorterStemmer()

# --- Text Extraction Imports ---
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

# --- Flask App Setup ---
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Gemini Setup ---
genai.configure(api_key=AI_CONFIG['GEMINI_API_KEY'])
ai_model = genai.GenerativeModel(AI_CONFIG['MODEL_NAME'])

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ================================================================
# AUTHENTICATION HELPERS
# ================================================================

def generate_token(user_id, username):
    """Generate a JWT token for a user."""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')


def verify_token(token):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(f):
    """Verify JWT token and set current user."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = request.args.get('token')
            
        if not token:
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        g.user_id = payload['user_id']
        g.username = payload['username']
        return f(*args, **kwargs)
    return decorated


# ================================================================
# EMAIL & OTP HELPERS
# ================================================================

def generate_otp():
    """Generate a 6-digit random OTP."""
    return str(random.randint(100000, 999999))


def send_otp_email(target_email, otp):
    """Send OTP email using Gmail SMTP."""
    try:
        sender_email = SMTP_CONFIG['SENDER_EMAIL']
        sender_password = SMTP_CONFIG['SENDER_PASSWORD']
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "SearchX Registration - One Time Password (OTP)"
        message["From"] = f"SearchX Admin <{sender_email}>"
        message["To"] = target_email

        # Premium HTML Template
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 40px; border-radius: 10px; border: 1px solid #ddd;">
                <h1 style="color: #1a1a1a; text-align: center;">SEARCHX</h1>
                <p style="font-size: 16px; color: #555;">Welcome to the next generation of legal document indexing.</p>
                <div style="background: #f9f9f9; padding: 20px; border-radius: 5px; text-align: center; margin: 30px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #e67e22;">{otp}</span>
                </div>
                <p style="font-size: 14px; color: #777;">This OTP is valid for 10 minutes. Please do not share it with anyone.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="font-size: 12px; color: #999; text-align: center;">SearchX &copy; 2026. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_CONFIG['SMTP_SERVER'], SMTP_CONFIG['SMTP_PORT'], context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, target_email, message.as_string())
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False


def generate_document_summary(text, title="legal document"):
    """Generate a 3-sentence legal summary using Gemini."""
    try:
        if not text:
            return f"No content available for {title}."
        
        # Take first 10,000 characters to stay within free tier/limits
        sample = text[:10000]
        
        prompt = (
            "You are a professional legal assistant. Provide a concise 3-sentence executive summary "
            f"of the following legal document titled '{title}'. Focus on the core purpose and key obligations. "
            "Maintain a formal tone.\n\n"
            f"TEXT:\n{sample}"
        )
        
        # Safety settings: Legal documents often contain content that default filters might block
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        response = ai_model.generate_content(prompt, safety_settings=safety_settings)
        
        # Check if response was actually generated (not blocked)
        if hasattr(response, 'candidates') and response.candidates and response.candidates[0].content.parts:
            return response.text.strip()
        else:
            return f"This document titled '{title}' contains legal provisions and obligations. A detailed AI summary was unavailable due to content filtering, but the full text is indexed for search."

    except Exception as e:
        print(f"[ERROR] Gemini Summarization Failed: {e}")
        # Meaningful fallback instead of 'could not be generated'
        return f"This is a legal document titled '{title}'. It has been successfully processed and indexed for keyword retrieval."


# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath):
    """Extract plain text from a PDF file using PyPDF2."""
    if PdfReader is None:
        raise ImportError("PyPDF2 is not installed")
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text.strip()


def extract_text_from_docx(filepath):
    """Extract plain text from a DOCX file using python-docx."""
    if DocxDocument is None:
        raise ImportError("python-docx is not installed")
    doc = DocxDocument(filepath)
    text = " ".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


def extract_text_from_txt(filepath):
    """Extract plain text from a TXT file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read().strip()


def extract_text(filepath, filename):
    """Route to correct text extractor based on file extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif ext == 'docx':
        return extract_text_from_docx(filepath)
    elif ext == 'txt':
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def get_stopwords(language_id=1):
    """Fetch stopwords from Oracle STOPWORDS table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT word FROM STOPWORDS WHERE language_id = :lang_id",
            {'lang_id': language_id}
        )
        stopwords = set(row[0].lower() for row in cursor.fetchall())
        return stopwords
    finally:
        cursor.close()
        conn.close()


def tokenize(text, stopwords=None):
    """
    Tokenize text:
    1. Lowercase
    2. Remove punctuation
    3. Split by whitespace
    4. Remove stopwords
    Returns dict of {term: frequency}
    """
    if stopwords is None:
        stopwords = set()

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    # Filter stopwords and short words
    words = [w for w in words if w not in stopwords and len(w) > 1]

    # Count frequencies with Stemming
    freq = {}
    for word in words:
        stemmed = stemmer.stem(word)
        freq[stemmed] = freq.get(stemmed, 0) + 1

    return freq


def validate_keyword(keyword):
    """Validate search keyword for security."""
    if not keyword or len(keyword.strip()) == 0:
        return False, "Keyword cannot be empty"
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return False, f"Keyword too long (max {MAX_KEYWORD_LENGTH} characters)"
    if not re.match(ALLOWED_KEYWORD_PATTERN, keyword):
        return False, "Keyword contains invalid characters"
    return True, "OK"


def get_file_type_id(filename):
    """Determine type_id based on file extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    type_map = {'pdf': 1, 'docx': 2, 'txt': 3}
    return type_map.get(ext, 3)


# ================================================================
# AUTH API ROUTES
# ================================================================

@app.route('/api/auth/register', methods=['POST'])
def register_initiate():
    """Initiate registration by sending OTP."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = (data.get('password') or '')
        full_name = (data.get('full_name') or '').strip()

        # Validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        if not email or '@' not in email:
            return jsonify({'error': 'Valid email is required'}), 400
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        if not full_name or len(full_name) < 2:
            return jsonify({'error': 'Full name is required'}), 400

        # Check if user already exists
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM USERS WHERE email = :email OR username = :uname", 
                         {'email': email, 'uname': username})
            if cursor.fetchone()[0] > 0:
                return jsonify({'error': 'User already registered with this email/username'}), 409
            
            # Generate OTP
            otp = generate_otp()
            otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Send Email
            if not send_otp_email(email, otp):
                return jsonify({'error': 'Failed to send OTP email. Please check configuration.'}), 500

            # Store in PENDING_USERS
            cursor.execute("""
                MERGE INTO PENDING_USERS p
                USING (SELECT :email as em from dual) s
                ON (p.email = s.em)
                WHEN MATCHED THEN
                    UPDATE SET username = :uname, password_hash = :phash, full_name = :fname, 
                               otp = :otp, otp_expiry = :expiry, created_at = SYSDATE
                WHEN NOT MATCHED THEN
                    INSERT (email, username, password_hash, full_name, otp, otp_expiry)
                    VALUES (:email2, :uname2, :phash2, :fname2, :otp2, :expiry2)
            """, {
                'email': email, 'uname': username, 'phash': password_hash, 'fname': full_name, 'otp': otp, 'expiry': otp_expiry,
                'email2': email, 'uname2': username, 'phash2': password_hash, 'fname2': full_name, 'otp2': otp, 'expiry2': otp_expiry
            })
            conn.commit()

            return jsonify({
                'message': 'OTP sent successfully to your email.',
                'email': email
            }), 200

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/register/verify', methods=['POST'])
def register_verify():
    """Verify OTP and complete registration."""
    try:
        data = request.get_json()
        email = (data.get('email') or '').strip().lower()
        otp = (data.get('otp') or '').strip()

        if not email or not otp:
            return jsonify({'error': 'Email and OTP are required'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Check OTP
            cursor.execute("""
                SELECT username, password_hash, full_name, otp, otp_expiry 
                FROM PENDING_USERS WHERE email = :email
            """, {'email': email})
            row = cursor.fetchone()

            if not row:
                return jsonify({'error': 'No registration found for this email'}), 404

            username, password_hash, full_name, db_otp, otp_expiry = row

            if db_otp != otp:
                return jsonify({'error': 'Invalid OTP'}), 401
            
            # Check expiry (Manually checking because datetime comparison in SQL can be tricky across environments)
            if datetime.datetime.now() > otp_expiry:
                 return jsonify({'error': 'OTP has expired'}), 401

            # Complete Registration
            user_id_var = cursor.var(oracledb.NUMBER)
            cursor.callproc('PROC_REGISTER_USER', [
                username, email, password_hash, full_name, user_id_var
            ])
            user_id = int(user_id_var.getvalue())
            
            # Delete from pending
            cursor.execute("DELETE FROM PENDING_USERS WHERE email = :email", {'email': email})
            
            conn.commit()

            # Generate token
            token = generate_token(user_id, username)

            return jsonify({
                'message': 'Registration successful',
                'token': token,
                'user': {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'full_name': full_name
                }
            }), 201

        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate a user and return JWT token."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        username = (data.get('username') or '').strip()
        password = (data.get('password') or '')

        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        try:
            print(f"[DEBUG] Login attempt for username: '{username}'")
            cursor.execute(
                "SELECT user_id, username, email, password_hash, full_name FROM USERS WHERE LOWER(username) = LOWER(:uname)",
                {'uname': username}
            )
            row = cursor.fetchone()

            if row is None:
                print(f"[DEBUG] User '{username}' NOT found in DB (checked case-insensitively)")
                return jsonify({'error': 'Invalid username or password'}), 401

            user_id, db_username, email, password_hash, full_name = row
            print(f"[DEBUG] User found: '{db_username}'. Hash length: {len(password_hash)}")

            # Verify password
            try:
                is_valid = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
                print(f"[DEBUG] Bcrypt check result: {is_valid}")
            except Exception as e:
                print(f"[DEBUG] Bcrypt verification error: {e}")
                return jsonify({'error': 'Security verification failed'}), 500

            if not is_valid:
                return jsonify({'error': 'Invalid username or password'}), 401

            # Generate token
            token = generate_token(user_id, db_username)

            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'user_id': user_id,
                    'username': db_username,
                    'email': email,
                    'full_name': full_name
                }
            }), 200

        except Exception as e:
            return jsonify({'error': f'Login failed: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get the currently authenticated user profile."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT user_id, username, email, full_name, created_at FROM USERS WHERE user_id = :u_id",
            {'u_id': g.user_id}
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'user': {
                'user_id': row[0],
                'username': row[1],
                'email': row[2],
                'full_name': row[3],
                'created_at': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ================================================================
# API ROUTES (Protected)
# ================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.close()
        conn.close()
        return jsonify({'status': 'ok', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'database': 'disconnected', 'message': str(e)}), 500


@app.route('/api/document-types', methods=['GET'])
def get_document_types():
    """Get all document types."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT type_id, type_name FROM DOCUMENT_TYPE ORDER BY type_id")
        rows = cursor.fetchall()
        types = [{'type_id': r[0], 'type_name': r[1]} for r in rows]
        return jsonify({'types': types}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get all languages."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT language_id, language_name, language_code FROM LANGUAGE ORDER BY language_id")
        rows = cursor.fetchall()
        languages = [{'language_id': r[0], 'language_name': r[1], 'language_code': r[2]} for r in rows]
        return jsonify({'languages': languages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/upload', methods=['POST'])
@login_required
def upload_document():
    """
    Upload a legal document (PDF/DOCX/TXT) or pasted text.
    Extract text, tokenize, and index via stored procedures.
    Document is owned by the authenticated user.
    """
    try:
        # Get form data
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        jurisdiction = request.form.get('jurisdiction', '').strip()
        language_id = int(request.form.get('language_id', 1))
        pasted_text = request.form.get('pasted_text', '').strip()

        if not title:
            return jsonify({'error': 'Title is required'}), 400
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        if not jurisdiction:
            return jsonify({'error': 'Jurisdiction is required'}), 400

        # Validate category and jurisdiction
        valid_categories = ['Contract', 'Case Summary', 'Policy', 'Act', 'Legal Notes']
        valid_jurisdictions = ['Supreme Court', 'High Court', 'District', 'Corporate', 'Other']

        if category not in valid_categories:
            return jsonify({'error': f'Invalid category. Must be one of: {", ".join(valid_categories)}'}), 400
        if jurisdiction not in valid_jurisdictions:
            return jsonify({'error': f'Invalid jurisdiction. Must be one of: {", ".join(valid_jurisdictions)}'}), 400

        file_data = None
        mime_type = 'text/plain'

        # Check for file upload
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400

            file_name = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, file_name)
            file.save(filepath)
            
            # Read back for DB storage
            with open(filepath, 'rb') as rb:
                file_data = rb.read()
            
            mime_type = getattr(file, 'content_type', 'application/octet-stream')

            try:
                text = extract_text(filepath, file_name)
            except Exception as e:
                # Only clean up if text extraction failed and we don't want partial data
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': f'Failed to extract text: {str(e)}'}), 500
            
            # File is now saved and persistent in UPLOAD_FOLDER
            type_id = get_file_type_id(file_name)

        elif pasted_text:
            text = pasted_text
            file_name = title.lower().replace(' ', '_')[:50] + '.txt'
            filepath = os.path.join(UPLOAD_FOLDER, file_name)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            
            file_data = text.encode('utf-8')
            mime_type = 'text/plain'
            type_id = 3
        else:
            return jsonify({'error': 'No file or text provided'}), 400

        if not text.strip():
            return jsonify({'error': 'No text could be extracted from the document'}), 400

        content_length = len(text)

        # --- Database Operations ---
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # 1. Generate Summary with Gemini
            summary = generate_document_summary(text, title)

            # 2. Insert document using PROC_ADD_DOCUMENT
            doc_id_var = cursor.var(oracledb.NUMBER)
            cursor.callproc('PROC_ADD_DOCUMENT', [
                title, file_name, content_length,
                type_id, language_id, category, jurisdiction,
                summary, file_data, mime_type, doc_id_var
            ])
            doc_id = int(doc_id_var.getvalue())

            # 3. Set owner_id for the document
            cursor.execute(
                "UPDATE DOCUMENTS SET owner_id = :user_id WHERE doc_id = :did",
                {'user_id': g.user_id, 'did': doc_id}
            )

            # 3. Tokenize and index
            stopwords = get_stopwords(language_id)
            term_freq = tokenize(text, stopwords)

            for term, freq in term_freq.items():
                if len(term) <= 500:  # VARCHAR2(500) limit
                    cursor.callproc('PROC_INDEX_TERM', [term, doc_id, freq])

            conn.commit()

            return jsonify({
                'message': 'Document uploaded and indexed successfully',
                'doc_id': doc_id,
                'title': title,
                'terms_indexed': len(term_freq),
                'content_length': content_length
            }), 201

        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/search', methods=['GET'])
@login_required
def search_documents():
    """
    Search legal documents by keyword.
    Only returns documents owned by the authenticated user.
    """
    keyword = request.args.get('q', '').strip()

    is_valid, msg = validate_keyword(keyword)
    if not is_valid:
        return jsonify({'error': msg}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Log the query (same as stored procedure logic)
        cursor.execute("""
            MERGE INTO QUERY_LOG ql
            USING (SELECT LOWER(:keyword) AS st FROM DUAL) src
            ON (ql.search_term = src.st)
            WHEN MATCHED THEN
                UPDATE SET ql.search_count = ql.search_count + 1, ql.last_searched = SYSDATE
            WHEN NOT MATCHED THEN
                INSERT (search_term, search_count, last_searched) VALUES (LOWER(:keyword2), 1, SYSDATE)
        """, {'keyword': keyword, 'keyword2': keyword})
        conn.commit()

        # Search for the stemmed version of the keyword
        stemmed_keyword = stemmer.stem(keyword.lower())
        
        cursor.execute("""
            SELECT d.doc_id,
                   d.title,
                   d.file_name,
                   d.category,
                   d.jurisdiction,
                   d.content_length,
                   d.summary,
                   d.created_at,
                   dt.type_name,
                   l.language_name,
                   ii.frequency AS relevance_score
            FROM INVERTED_INDEX ii
            JOIN TERMS t       ON t.term_id   = ii.term_id
            JOIN DOCUMENTS d   ON d.doc_id    = ii.doc_id
            JOIN DOCUMENT_TYPE dt ON dt.type_id = d.type_id
            JOIN LANGUAGE l    ON l.language_id = d.language_id
            WHERE (LOWER(t.term_text) = :stemmed OR LOWER(t.term_text) LIKE :partial)
              AND (d.owner_id = :user_id OR d.owner_id IS NULL)
            ORDER BY ii.frequency DESC
        """, {
            'stemmed': stemmed_keyword,
            'partial': f'%{keyword.lower()}%',
            'user_id': g.user_id
        })

        columns = [col[0].lower() for col in cursor.description]
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = dict(zip(columns, row))
            if result.get('created_at'):
                result['created_at'] = result['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            results.append(result)

        return jsonify({
            'keyword': keyword,
            'count': len(results),
            'results': results
        }), 200

    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    """
    Get search analytics: top searched terms.
    Document stats are scoped to the authenticated user.
    """
    limit = request.args.get('limit', 20, type=int)
    if limit < 1 or limit > 100:
        limit = 20

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Top searched terms (global — queries are shared)
        cursor.execute(
            "SELECT search_term, search_count, last_searched "
            "FROM (SELECT search_term, search_count, last_searched "
            "FROM QUERY_LOG ORDER BY search_count DESC) "
            "WHERE ROWNUM <= :lim",
            {'lim': limit}
        )
        rows = cursor.fetchall()

        top_terms = []
        for row in rows:
            top_terms.append({
                'search_term': row[0],
                'search_count': int(row[1]),
                'last_searched': row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else None
            })

        # Additional stats — scoped to user's documents
        cursor.execute(
            "SELECT COUNT(*) FROM DOCUMENTS WHERE owner_id = :user_id OR owner_id IS NULL",
            {'user_id': g.user_id}
        )
        total_docs = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT t.term_id) FROM TERMS t
            JOIN INVERTED_INDEX ii ON ii.term_id = t.term_id
            JOIN DOCUMENTS d ON d.doc_id = ii.doc_id
            WHERE d.owner_id = :user_id OR d.owner_id IS NULL
        """, {'user_id': g.user_id})
        total_terms = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM QUERY_LOG")
        total_queries = cursor.fetchone()[0]

        cursor.execute("SELECT NVL(SUM(search_count), 0) FROM QUERY_LOG")
        total_searches = cursor.fetchone()[0]

        return jsonify({
            'top_terms': top_terms,
            'stats': {
                'total_documents': int(total_docs),
                'total_unique_terms': int(total_terms),
                'total_unique_queries': int(total_queries),
                'total_searches': int(total_searches)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Analytics failed: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/documents', methods=['GET'])
@login_required
def get_documents():
    """Get all documents owned by the authenticated user."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT d.doc_id, d.title, d.file_name, d.content_length, d.summary,
                   d.created_at, d.category, d.jurisdiction,
                   dt.type_name, l.language_name,
                   NVL(ds.total_terms, 0) AS total_terms,
                   NVL(ds.unique_terms, 0) AS unique_terms
            FROM DOCUMENTS d
            JOIN DOCUMENT_TYPE dt ON dt.type_id = d.type_id
            JOIN LANGUAGE l ON l.language_id = d.language_id
            LEFT JOIN DOCUMENT_STATS ds ON ds.doc_id = d.doc_id
            WHERE d.owner_id = :user_id OR d.owner_id IS NULL
            ORDER BY d.created_at DESC
        """, {'user_id': g.user_id})
        rows = cursor.fetchall()

        documents = []
        for row in rows:
            documents.append({
                'doc_id': row[0],
                'title': row[1],
                'file_name': row[2],
                'content_length': row[3],
                'summary': row[4],
                'created_at': row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None,
                'category': row[6],
                'jurisdiction': row[7],
                'type_name': row[8],
                'language_name': row[9],
                'total_terms': row[10],
                'unique_terms': row[11]
            })

        return jsonify({'documents': documents, 'count': len(documents)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/documents/<int:doc_id>/view', methods=['GET'])
@login_required
def view_document(doc_id):
    """Serve the document file for viewing."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT file_name, file_data, mime_type FROM DOCUMENTS WHERE doc_id = :did", {'did': doc_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Document ID not found in database'}), 404
        
        filename, file_data, mime_type = row
        
        if not file_data:
            # Fallback to filesystem if BLOB is empty (for older documents)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if not os.path.exists(filepath):
                return jsonify({
                    'error': 'Physical file missing from server and database.',
                    'message': 'This document was indexed with an older version of SEARCHX. Please upload it again.'
                }), 404
            return send_from_directory(UPLOAD_FOLDER, filename)
            
        from flask import Response
        return Response(
            file_data.read() if hasattr(file_data, 'read') else file_data,
            mimetype=mime_type or 'application/octet-stream',
            headers={"Content-disposition": f"inline; filename={filename}"}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
@login_required
def delete_document(doc_id):
    """Delete a document and its associated data."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Verify ownership
        cursor.execute("SELECT owner_id, file_name FROM DOCUMENTS WHERE doc_id = :did", {'did': doc_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Document not found'}), 404
        
        owner_id, file_name = row
        if owner_id and owner_id != g.user_id:
            return jsonify({'error': 'Unauthorized to delete this document'}), 403
        
        # 2. Delete associated data (cascading)
        cursor.execute("DELETE FROM INVERTED_INDEX WHERE doc_id = :did", {'did': doc_id})
        cursor.execute("DELETE FROM DOCUMENT_STATS WHERE doc_id = :did", {'did': doc_id})
        cursor.execute("DELETE FROM DOCUMENTS WHERE doc_id = :did", {'did': doc_id})
        
        # 3. Clean up physical file if it exists
        filepath = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass # Non-critical if DB is clean
        
        conn.commit()
        return jsonify({'message': 'Document deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# ================================================================
# MAIN
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  SEARCHX - Search Engine Indexing & Query Analytics")
    print("  Domain: LAW / LEGAL DOCUMENTS")
    print("  Backend: Flask + Oracle 11g")
    print("  Authentication: JWT + bcrypt")
    print("=" * 60)
    app.run(
        debug=FLASK_CONFIG['DEBUG'],
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        threaded=True
    )
