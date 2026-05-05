-- ============================================================
-- SEARCHX: Schema Fix Script (V2)
-- Adds missing 'summary' column, updates procedures, and adds PENDING_USERS
-- ============================================================

-- 1. Add SUMMARY column to DOCUMENTS if it doesn't exist
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM user_tab_columns
    WHERE table_name = 'DOCUMENTS' AND column_name = 'SUMMARY';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD (summary CLOB)';
    END IF;
END;
/

-- 2. Update PROC_ADD_DOCUMENT to include summary
CREATE OR REPLACE PROCEDURE PROC_ADD_DOCUMENT (
    p_title        IN  VARCHAR2,
    p_file_name    IN  VARCHAR2,
    p_content_len  IN  NUMBER,
    p_type_id      IN  NUMBER,
    p_language_id  IN  NUMBER,
    p_category     IN  VARCHAR2,
    p_jurisdiction IN  VARCHAR2,
    p_summary      IN  CLOB,
    p_doc_id       OUT NUMBER
) AS
BEGIN
    SELECT SEQ_DOCUMENT.NEXTVAL INTO p_doc_id FROM DUAL;

    INSERT INTO DOCUMENTS (
        doc_id, title, file_name, content_length, created_at, 
        type_id, language_id, category, jurisdiction, summary
    )
    VALUES (
        p_doc_id, p_title, p_file_name, p_content_len, SYSDATE, 
        p_type_id, p_language_id, p_category, p_jurisdiction, p_summary
    );

    -- Create corresponding DOCUMENT_STATS row
    INSERT INTO DOCUMENT_STATS (doc_id, total_terms, unique_terms, last_indexed)
    VALUES (p_doc_id, 0, 0, NULL);

    COMMIT;
END;
/

-- 3. Update PROC_SEARCH_DOCUMENTS to include summary
CREATE OR REPLACE PROCEDURE PROC_SEARCH_DOCUMENTS (
    p_keyword   IN  VARCHAR2,
    p_results   OUT SYS_REFCURSOR
) AS
BEGIN
    -- Log the query
    MERGE INTO QUERY_LOG ql
    USING (SELECT LOWER(p_keyword) AS st FROM DUAL) src
    ON (ql.search_term = src.st)
    WHEN MATCHED THEN
        UPDATE SET ql.search_count = ql.search_count + 1, ql.last_searched = SYSDATE
    WHEN NOT MATCHED THEN
        INSERT (search_term, search_count, last_searched) VALUES (LOWER(p_keyword), 1, SYSDATE);

    COMMIT;

    -- Return ranked results
    OPEN p_results FOR
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
        WHERE LOWER(t.term_text) = LOWER(p_keyword)
        ORDER BY ii.frequency DESC;
END;
/

-- 4. Ensure owner_id is handled
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM user_tab_columns
    WHERE table_name = 'DOCUMENTS' AND column_name = 'OWNER_ID';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD (owner_id NUMBER)';
    END IF;
END;
/

-- 5. Create PENDING_USERS table for OTP Auth
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM user_tables WHERE table_name = 'PENDING_USERS';
    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE TABLE PENDING_USERS (
            email         VARCHAR2(255) PRIMARY KEY,
            username      VARCHAR2(100) NOT NULL,
            password_hash VARCHAR2(500) NOT NULL,
            full_name     VARCHAR2(200) NOT NULL,
            otp           VARCHAR2(10)  NOT NULL,
            otp_expiry    TIMESTAMP     NOT NULL,
            created_at    DATE          DEFAULT SYSDATE NOT NULL
        )';
    END IF;
END;
/

COMMIT;
