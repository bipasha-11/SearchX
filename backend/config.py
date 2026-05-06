"""
SEARCHX Configuration
Oracle 11g Database Connection Settings
"""

import os

# Oracle Database Configuration
ORACLE_CONFIG = {
    'user': os.environ.get('ORACLE_USER', 'searchx'),
    'password': os.environ.get('ORACLE_PASSWORD', 'searchx123'),
    'dsn': os.environ.get('ORACLE_DSN', 'localhost:1521/XE'),
}

# Flask Configuration
FLASK_CONFIG = {
    'DEBUG': os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
    'HOST': os.environ.get('FLASK_HOST', '0.0.0.0'),
    'PORT': int(os.environ.get('FLASK_PORT', 5000)),
}

# ... (rest stays similar but with environ checks)

# Upload Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'))
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max

# Security
MAX_KEYWORD_LENGTH = 100
ALLOWED_KEYWORD_PATTERN = r'^[a-zA-Z0-9\s\-_\.,\(\)\[\]]+$'

# SMTP Configuration (SendGrid Bypass for Render)
SMTP_CONFIG = {
    'SENDER_EMAIL': os.environ.get('SMTP_EMAIL', 'noreplyemail042@gmail.com'),
    'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY'),
}

# AI Configuration (Google Gemini)
AI_CONFIG = {
    'GEMINI_API_KEY': os.environ.get('GEMINI_API_KEY'),
    'MODEL_NAME': 'gemini-flash-latest',
}

# JWT Authentication
JWT_SECRET = os.environ.get('JWT_SECRET', 'searchx-prod-secret-change-me')
JWT_EXPIRY_HOURS = int(os.environ.get('JWT_EXPIRY_HOURS', 24))

