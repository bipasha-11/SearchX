-- ============================================================
-- SEARCHX: Search Engine Indexing & Query Analytics System
-- Oracle 11g DDL Script
-- Domain: LAW / LEGAL DOCUMENTS
-- ============================================================

-- ============================================================
-- 1. DROP EXISTING OBJECTS (clean slate)
-- ============================================================
BEGIN
    FOR r IN (SELECT table_name FROM user_tables WHERE table_name IN (
        'DOCUMENT_STATS','QUERY_LOG','INVERTED_INDEX','STOPWORDS',
        'TERMS','DOCUMENTS','LANGUAGE','DOCUMENT_TYPE'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || r.table_name || ' CASCADE CONSTRAINTS';
    END LOOP;
END;
/

BEGIN
    FOR r IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN (
        'SEQ_DOC_TYPE','SEQ_LANGUAGE','SEQ_DOCUMENT','SEQ_TERM',
        'SEQ_QUERY_LOG','SEQ_STOPWORD','SEQ_DOC_STATS'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || r.sequence_name;
    END LOOP;
END;
/

-- ============================================================
-- 2. SEQUENCES
-- ============================================================
CREATE SEQUENCE SEQ_DOC_TYPE    START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_LANGUAGE    START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_DOCUMENT    START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_TERM        START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_QUERY_LOG   START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_STOPWORD    START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE SEQ_DOC_STATS   START WITH 1 INCREMENT BY 1 NOCACHE;

-- ============================================================
-- 3. TABLES
-- ============================================================

-- 3.1 DOCUMENT_TYPE
CREATE TABLE DOCUMENT_TYPE (
    type_id     NUMBER        PRIMARY KEY,
    type_name   VARCHAR2(100) NOT NULL UNIQUE,
    description VARCHAR2(500)
);

-- 3.2 LANGUAGE
CREATE TABLE LANGUAGE (
    language_id   NUMBER        PRIMARY KEY,
    language_name VARCHAR2(100) NOT NULL UNIQUE,
    language_code VARCHAR2(10)  NOT NULL UNIQUE
);

-- 3.3 DOCUMENTS
CREATE TABLE DOCUMENTS (
    doc_id         NUMBER        PRIMARY KEY,
    title          VARCHAR2(500) NOT NULL,
    file_name      VARCHAR2(500) NOT NULL,
    content_length NUMBER        NOT NULL,
    created_at     DATE          DEFAULT SYSDATE NOT NULL,
    type_id        NUMBER        NOT NULL,
    language_id    NUMBER        NOT NULL,
    category       VARCHAR2(50)  NOT NULL,
    jurisdiction   VARCHAR2(50)  NOT NULL,
    CONSTRAINT fk_doc_type     FOREIGN KEY (type_id)     REFERENCES DOCUMENT_TYPE(type_id),
    CONSTRAINT fk_doc_lang     FOREIGN KEY (language_id)  REFERENCES LANGUAGE(language_id),
    CONSTRAINT chk_category    CHECK (category IN ('Contract','Case Summary','Policy','Act','Legal Notes')),
    CONSTRAINT chk_jurisdiction CHECK (jurisdiction IN ('Supreme Court','High Court','District','Corporate','Other')),
    CONSTRAINT chk_content_len CHECK (content_length >= 0)
);

-- 3.4 TERMS
CREATE TABLE TERMS (
    term_id   NUMBER        PRIMARY KEY,
    term_text VARCHAR2(500) NOT NULL UNIQUE
);

-- 3.5 INVERTED_INDEX (composite PK)
CREATE TABLE INVERTED_INDEX (
    term_id   NUMBER NOT NULL,
    doc_id    NUMBER NOT NULL,
    frequency NUMBER DEFAULT 1 NOT NULL,
    CONSTRAINT pk_inverted_index PRIMARY KEY (term_id, doc_id),
    CONSTRAINT fk_ii_term FOREIGN KEY (term_id) REFERENCES TERMS(term_id),
    CONSTRAINT fk_ii_doc  FOREIGN KEY (doc_id)  REFERENCES DOCUMENTS(doc_id),
    CONSTRAINT chk_frequency CHECK (frequency > 0)
);

-- 3.6 QUERY_LOG
CREATE TABLE QUERY_LOG (
    query_id      NUMBER        PRIMARY KEY,
    search_term   VARCHAR2(500) NOT NULL UNIQUE,
    search_count  NUMBER        DEFAULT 1 NOT NULL,
    last_searched DATE          DEFAULT SYSDATE NOT NULL
);

-- 3.7 STOPWORDS (unique per language)
CREATE TABLE STOPWORDS (
    stopword_id NUMBER        PRIMARY KEY,
    word        VARCHAR2(100) NOT NULL,
    language_id NUMBER        NOT NULL,
    CONSTRAINT fk_sw_lang     FOREIGN KEY (language_id) REFERENCES LANGUAGE(language_id),
    CONSTRAINT uq_stopword    UNIQUE (word, language_id)
);

-- 3.8 DOCUMENT_STATS (1:1 with DOCUMENTS)
CREATE TABLE DOCUMENT_STATS (
    stat_id        NUMBER PRIMARY KEY,
    doc_id         NUMBER NOT NULL UNIQUE,
    total_terms    NUMBER DEFAULT 0 NOT NULL,
    unique_terms   NUMBER DEFAULT 0 NOT NULL,
    last_indexed   DATE   DEFAULT SYSDATE,
    CONSTRAINT fk_ds_doc FOREIGN KEY (doc_id) REFERENCES DOCUMENTS(doc_id)
);

-- ============================================================
-- 4. INDEXES for search performance
-- ============================================================
CREATE INDEX idx_terms_text       ON TERMS(term_text);
CREATE INDEX idx_docs_title       ON DOCUMENTS(title);
CREATE INDEX idx_docs_category    ON DOCUMENTS(category);
CREATE INDEX idx_docs_jurisdiction ON DOCUMENTS(jurisdiction);
CREATE INDEX idx_query_log_term   ON QUERY_LOG(search_term);
CREATE INDEX idx_ii_doc           ON INVERTED_INDEX(doc_id);

-- ============================================================
-- 5. TRIGGERS
-- ============================================================

-- 5.1 Auto-generate DOCUMENT_TYPE ID
CREATE OR REPLACE TRIGGER trg_doc_type_id
BEFORE INSERT ON DOCUMENT_TYPE
FOR EACH ROW
BEGIN
    IF :NEW.type_id IS NULL THEN
        SELECT SEQ_DOC_TYPE.NEXTVAL INTO :NEW.type_id FROM DUAL;
    END IF;
END;
/

-- 5.2 Auto-generate LANGUAGE ID
CREATE OR REPLACE TRIGGER trg_language_id
BEFORE INSERT ON LANGUAGE
FOR EACH ROW
BEGIN
    IF :NEW.language_id IS NULL THEN
        SELECT SEQ_LANGUAGE.NEXTVAL INTO :NEW.language_id FROM DUAL;
    END IF;
END;
/

-- 5.3 Auto-generate DOCUMENT ID
CREATE OR REPLACE TRIGGER trg_document_id
BEFORE INSERT ON DOCUMENTS
FOR EACH ROW
BEGIN
    IF :NEW.doc_id IS NULL THEN
        SELECT SEQ_DOCUMENT.NEXTVAL INTO :NEW.doc_id FROM DUAL;
    END IF;
END;
/

-- 5.4 Validate content_length not negative
CREATE OR REPLACE TRIGGER trg_validate_content_length
BEFORE INSERT OR UPDATE ON DOCUMENTS
FOR EACH ROW
BEGIN
    IF :NEW.content_length < 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'content_length cannot be negative');
    END IF;
END;
/

-- 5.5 Auto-generate TERM ID
CREATE OR REPLACE TRIGGER trg_term_id
BEFORE INSERT ON TERMS
FOR EACH ROW
BEGIN
    IF :NEW.term_id IS NULL THEN
        SELECT SEQ_TERM.NEXTVAL INTO :NEW.term_id FROM DUAL;
    END IF;
END;
/

-- 5.6 Auto-generate QUERY_LOG ID
CREATE OR REPLACE TRIGGER trg_query_log_id
BEFORE INSERT ON QUERY_LOG
FOR EACH ROW
BEGIN
    IF :NEW.query_id IS NULL THEN
        SELECT SEQ_QUERY_LOG.NEXTVAL INTO :NEW.query_id FROM DUAL;
    END IF;
END;
/

-- 5.7 Auto-generate STOPWORD ID
CREATE OR REPLACE TRIGGER trg_stopword_id
BEFORE INSERT ON STOPWORDS
FOR EACH ROW
BEGIN
    IF :NEW.stopword_id IS NULL THEN
        SELECT SEQ_STOPWORD.NEXTVAL INTO :NEW.stopword_id FROM DUAL;
    END IF;
END;
/

-- 5.8 Auto-generate DOCUMENT_STATS ID
CREATE OR REPLACE TRIGGER trg_doc_stats_id
BEFORE INSERT ON DOCUMENT_STATS
FOR EACH ROW
BEGIN
    IF :NEW.stat_id IS NULL THEN
        SELECT SEQ_DOC_STATS.NEXTVAL INTO :NEW.stat_id FROM DUAL;
    END IF;
END;
/

-- 5.9 Update DOCUMENT_STATS.last_indexed when inverted index changes
CREATE OR REPLACE TRIGGER trg_update_last_indexed
AFTER INSERT OR UPDATE ON INVERTED_INDEX
FOR EACH ROW
BEGIN
    UPDATE DOCUMENT_STATS
    SET last_indexed = SYSDATE
    WHERE doc_id = :NEW.doc_id;
END;
/

-- ============================================================
-- 6. STORED PROCEDURES
-- ============================================================

-- 6.1 PROC_ADD_DOCUMENT
CREATE OR REPLACE PROCEDURE PROC_ADD_DOCUMENT (
    p_title        IN  VARCHAR2,
    p_file_name    IN  VARCHAR2,
    p_content_len  IN  NUMBER,
    p_type_id      IN  NUMBER,
    p_language_id  IN  NUMBER,
    p_category     IN  VARCHAR2,
    p_jurisdiction IN  VARCHAR2,
    p_doc_id       OUT NUMBER
) AS
BEGIN
    SELECT SEQ_DOCUMENT.NEXTVAL INTO p_doc_id FROM DUAL;

    INSERT INTO DOCUMENTS (doc_id, title, file_name, content_length, created_at, type_id, language_id, category, jurisdiction)
    VALUES (p_doc_id, p_title, p_file_name, p_content_len, SYSDATE, p_type_id, p_language_id, p_category, p_jurisdiction);

    -- Create corresponding DOCUMENT_STATS row
    INSERT INTO DOCUMENT_STATS (doc_id, total_terms, unique_terms, last_indexed)
    VALUES (p_doc_id, 0, 0, NULL);

    COMMIT;
END;
/

-- 6.2 PROC_INDEX_TERM
CREATE OR REPLACE PROCEDURE PROC_INDEX_TERM (
    p_term_text IN VARCHAR2,
    p_doc_id    IN NUMBER,
    p_frequency IN NUMBER
) AS
    v_term_id NUMBER;
BEGIN
    -- Insert term if not exists
    BEGIN
        SELECT term_id INTO v_term_id FROM TERMS WHERE term_text = p_term_text;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SELECT SEQ_TERM.NEXTVAL INTO v_term_id FROM DUAL;
            INSERT INTO TERMS (term_id, term_text) VALUES (v_term_id, p_term_text);
    END;

    -- MERGE into inverted index
    MERGE INTO INVERTED_INDEX ii
    USING (SELECT v_term_id AS tid, p_doc_id AS did FROM DUAL) src
    ON (ii.term_id = src.tid AND ii.doc_id = src.did)
    WHEN MATCHED THEN
        UPDATE SET ii.frequency = p_frequency
    WHEN NOT MATCHED THEN
        INSERT (term_id, doc_id, frequency) VALUES (v_term_id, p_doc_id, p_frequency);

    -- Update document stats
    UPDATE DOCUMENT_STATS
    SET total_terms  = (SELECT NVL(SUM(frequency), 0) FROM INVERTED_INDEX WHERE doc_id = p_doc_id),
        unique_terms = (SELECT COUNT(*) FROM INVERTED_INDEX WHERE doc_id = p_doc_id),
        last_indexed = SYSDATE
    WHERE doc_id = p_doc_id;

    COMMIT;
END;
/

-- 6.3 PROC_SEARCH_DOCUMENTS
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

-- 6.4 PROC_GET_TOP_TERMS
CREATE OR REPLACE PROCEDURE PROC_GET_TOP_TERMS (
    p_limit   IN  NUMBER,
    p_results OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_results FOR
        SELECT search_term, search_count, last_searched
        FROM (
            SELECT search_term, search_count, last_searched
            FROM QUERY_LOG
            ORDER BY search_count DESC
        )
        WHERE ROWNUM <= p_limit;
END;
/

-- 6.5 PROC_GET_DOC_STATS
CREATE OR REPLACE PROCEDURE PROC_GET_DOC_STATS (
    p_doc_id  IN  NUMBER,
    p_results OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_results FOR
        SELECT ds.stat_id,
               ds.doc_id,
               d.title,
               d.file_name,
               d.category,
               d.jurisdiction,
               ds.total_terms,
               ds.unique_terms,
               ds.last_indexed,
               d.content_length,
               d.created_at
        FROM DOCUMENT_STATS ds
        JOIN DOCUMENTS d ON d.doc_id = ds.doc_id
        WHERE ds.doc_id = p_doc_id;
END;
/

-- Verification
SELECT 'Schema created successfully' AS status FROM DUAL;
