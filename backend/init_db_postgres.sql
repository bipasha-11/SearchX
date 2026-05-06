-- SEARCHX Database Schema (PostgreSQL)

-- Users Table
CREATE TABLE IF NOT EXISTS USERS (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    otp VARCHAR(10),
    otp_expiry TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pending Users (for OTP)
CREATE TABLE IF NOT EXISTS PENDING_USERS (
    email VARCHAR(100) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    otp VARCHAR(10),
    otp_expiry TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Documents Table
CREATE TABLE IF NOT EXISTS DOCUMENTS (
    doc_id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES USERS(user_id),
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255),
    file_type_id INTEGER,
    language_id INTEGER DEFAULT 1,
    category VARCHAR(100),
    jurisdiction VARCHAR(100),
    content_length INTEGER,
    mime_type VARCHAR(100),
    file_data BYTEA,
    summary TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inverted Index Table
CREATE TABLE IF NOT EXISTS INVERTED_INDEX (
    word VARCHAR(500) NOT NULL,
    doc_id INTEGER REFERENCES DOCUMENTS(doc_id) ON DELETE CASCADE,
    frequency INTEGER DEFAULT 1,
    PRIMARY KEY (word, doc_id)
);

-- Search Query Logs (User-specific)
CREATE TABLE IF NOT EXISTS QUERY_LOGS (
    search_term VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES USERS(user_id) ON DELETE CASCADE,
    search_count INTEGER DEFAULT 1,
    last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (search_term, user_id)
);

-- Stopwords Table
CREATE TABLE IF NOT EXISTS STOPWORDS (
    word VARCHAR(100) PRIMARY KEY,
    language_id INTEGER DEFAULT 1
);

-- Insert common English stopwords
INSERT INTO STOPWORDS (word, language_id) VALUES 
('the', 1), ('is', 1), ('at', 1), ('which', 1), ('on', 1), ('and', 1), ('a', 1), ('an', 1), 
('of', 1), ('to', 1), ('in', 1), ('for', 1), ('with', 1), ('by', 1), ('as', 1), ('be', 1), 
('that', 1), ('this', 1), ('from', 1), ('it', 1), ('not', 1), ('or', 1)
ON CONFLICT DO NOTHING;
