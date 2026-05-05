-- ============================================================
-- SEARCHX: File Storage Fix
-- Adds BLOB column to DOCUMENTS for persistent file storage
-- ============================================================

-- 1. Add FILE_DATA and MIME_TYPE columns
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM user_tab_columns
    WHERE table_name = 'DOCUMENTS' AND column_name = 'FILE_DATA';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD (file_data BLOB)';
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM user_tab_columns
    WHERE table_name = 'DOCUMENTS' AND column_name = 'MIME_TYPE';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD (mime_type VARCHAR2(100))';
    END IF;
END;
/

-- 2. Update PROC_ADD_DOCUMENT to include file_data and mime_type
CREATE OR REPLACE PROCEDURE PROC_ADD_DOCUMENT (
    p_title        IN  VARCHAR2,
    p_file_name    IN  VARCHAR2,
    p_content_len  IN  NUMBER,
    p_type_id      IN  NUMBER,
    p_language_id  IN  NUMBER,
    p_category     IN  VARCHAR2,
    p_jurisdiction IN  VARCHAR2,
    p_summary      IN  CLOB,
    p_file_data    IN  BLOB,
    p_mime_type    IN  VARCHAR2,
    p_doc_id       OUT NUMBER
) AS
BEGIN
    SELECT SEQ_DOCUMENT.NEXTVAL INTO p_doc_id FROM DUAL;

    INSERT INTO DOCUMENTS (
        doc_id, title, file_name, content_length, created_at, 
        type_id, language_id, category, jurisdiction, summary,
        file_data, mime_type
    )
    VALUES (
        p_doc_id, p_title, p_file_name, p_content_len, SYSDATE, 
        p_type_id, p_language_id, p_category, p_jurisdiction, p_summary,
        p_file_data, p_mime_type
    );

    -- Create corresponding DOCUMENT_STATS row
    INSERT INTO DOCUMENT_STATS (doc_id, total_terms, unique_terms, last_indexed)
    VALUES (p_doc_id, 0, 0, NULL);

    COMMIT;
END;
/

COMMIT;
