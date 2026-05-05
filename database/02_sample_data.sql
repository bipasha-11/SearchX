-- ============================================================
-- SEARCHX: Sample Data Insertion
-- Domain: LAW / LEGAL DOCUMENTS
-- ============================================================

-- ============================================================
-- 1. DOCUMENT_TYPE
-- ============================================================
INSERT INTO DOCUMENT_TYPE (type_id, type_name, description) VALUES (SEQ_DOC_TYPE.NEXTVAL, 'PDF', 'Portable Document Format');
INSERT INTO DOCUMENT_TYPE (type_id, type_name, description) VALUES (SEQ_DOC_TYPE.NEXTVAL, 'DOCX', 'Microsoft Word Document');
INSERT INTO DOCUMENT_TYPE (type_id, type_name, description) VALUES (SEQ_DOC_TYPE.NEXTVAL, 'TXT', 'Plain Text File');
COMMIT;

-- ============================================================
-- 2. LANGUAGE
-- ============================================================
INSERT INTO LANGUAGE (language_id, language_name, language_code) VALUES (SEQ_LANGUAGE.NEXTVAL, 'English', 'EN');
INSERT INTO LANGUAGE (language_id, language_name, language_code) VALUES (SEQ_LANGUAGE.NEXTVAL, 'Hindi', 'HI');
INSERT INTO LANGUAGE (language_id, language_name, language_code) VALUES (SEQ_LANGUAGE.NEXTVAL, 'Tamil', 'TA');
COMMIT;

-- ============================================================
-- 3. STOPWORDS (English)
-- ============================================================
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'the', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'is', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'at', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'which', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'on', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'a', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'an', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'and', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'or', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'in', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'of', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'to', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'for', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'with', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'by', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'from', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'as', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'it', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'this', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'that', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'was', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'are', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'be', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'has', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'have', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'not', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'but', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'been', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'were', 1);
INSERT INTO STOPWORDS (stopword_id, word, language_id) VALUES (SEQ_STOPWORD.NEXTVAL, 'shall', 1);
COMMIT;

-- ============================================================
-- 4. DOCUMENTS (using stored procedure)
-- ============================================================
DECLARE
    v_doc_id NUMBER;
BEGIN
    PROC_ADD_DOCUMENT('Indian Contract Act 1872 - Overview', 'indian_contract_act.pdf', 15420, 1, 1, 'Act', 'Supreme Court', v_doc_id);
    PROC_ADD_DOCUMENT('Kesavananda Bharati v State of Kerala', 'kesavananda_bharati.pdf', 28340, 1, 1, 'Case Summary', 'Supreme Court', v_doc_id);
    PROC_ADD_DOCUMENT('Employee Non-Disclosure Agreement', 'nda_template.docx', 4520, 2, 1, 'Contract', 'Corporate', v_doc_id);
    PROC_ADD_DOCUMENT('Data Protection Policy 2023', 'data_protection_policy.pdf', 8930, 1, 1, 'Policy', 'Corporate', v_doc_id);
    PROC_ADD_DOCUMENT('Right to Information Act 2005', 'rti_act_2005.pdf', 19870, 1, 1, 'Act', 'Supreme Court', v_doc_id);
    PROC_ADD_DOCUMENT('Motor Vehicles Act Amendment Notes', 'mv_act_notes.txt', 6210, 3, 1, 'Legal Notes', 'High Court', v_doc_id);
    PROC_ADD_DOCUMENT('Bail Application Format - Sessions Court', 'bail_application.docx', 3150, 2, 1, 'Legal Notes', 'District', v_doc_id);
    PROC_ADD_DOCUMENT('Intellectual Property Rights Policy', 'ipr_policy.pdf', 11200, 1, 1, 'Policy', 'Corporate', v_doc_id);
    PROC_ADD_DOCUMENT('Consumer Protection Act 2019 Summary', 'consumer_protection.pdf', 14500, 1, 1, 'Case Summary', 'High Court', v_doc_id);
    PROC_ADD_DOCUMENT('Commercial Lease Agreement Template', 'lease_agreement.docx', 7650, 2, 1, 'Contract', 'Corporate', v_doc_id);
END;
/

-- ============================================================
-- 5. TERMS + INVERTED_INDEX (using stored procedure)
-- ============================================================
DECLARE
BEGIN
    -- Legal terms indexed across documents
    PROC_INDEX_TERM('contract', 1, 12);
    PROC_INDEX_TERM('agreement', 1, 8);
    PROC_INDEX_TERM('obligation', 1, 6);
    PROC_INDEX_TERM('breach', 1, 4);
    PROC_INDEX_TERM('consideration', 1, 7);
    PROC_INDEX_TERM('parties', 1, 9);

    PROC_INDEX_TERM('fundamental', 2, 15);
    PROC_INDEX_TERM('rights', 2, 18);
    PROC_INDEX_TERM('constitution', 2, 22);
    PROC_INDEX_TERM('amendment', 2, 11);
    PROC_INDEX_TERM('parliament', 2, 8);
    PROC_INDEX_TERM('judiciary', 2, 6);

    PROC_INDEX_TERM('confidential', 3, 14);
    PROC_INDEX_TERM('disclosure', 3, 10);
    PROC_INDEX_TERM('agreement', 3, 7);
    PROC_INDEX_TERM('parties', 3, 5);
    PROC_INDEX_TERM('proprietary', 3, 8);

    PROC_INDEX_TERM('data', 4, 20);
    PROC_INDEX_TERM('protection', 4, 16);
    PROC_INDEX_TERM('privacy', 4, 12);
    PROC_INDEX_TERM('consent', 4, 9);
    PROC_INDEX_TERM('processing', 4, 7);

    PROC_INDEX_TERM('information', 5, 25);
    PROC_INDEX_TERM('rights', 5, 14);
    PROC_INDEX_TERM('authority', 5, 10);
    PROC_INDEX_TERM('disclosure', 5, 8);
    PROC_INDEX_TERM('citizen', 5, 6);

    PROC_INDEX_TERM('vehicle', 6, 11);
    PROC_INDEX_TERM('license', 6, 8);
    PROC_INDEX_TERM('penalty', 6, 6);
    PROC_INDEX_TERM('amendment', 6, 9);
    PROC_INDEX_TERM('regulation', 6, 5);

    PROC_INDEX_TERM('bail', 7, 15);
    PROC_INDEX_TERM('accused', 7, 10);
    PROC_INDEX_TERM('court', 7, 12);
    PROC_INDEX_TERM('custody', 7, 7);
    PROC_INDEX_TERM('surety', 7, 4);

    PROC_INDEX_TERM('intellectual', 8, 13);
    PROC_INDEX_TERM('property', 8, 16);
    PROC_INDEX_TERM('patent', 8, 9);
    PROC_INDEX_TERM('trademark', 8, 7);
    PROC_INDEX_TERM('copyright', 8, 11);

    PROC_INDEX_TERM('consumer', 9, 19);
    PROC_INDEX_TERM('protection', 9, 14);
    PROC_INDEX_TERM('complaint', 9, 8);
    PROC_INDEX_TERM('redressal', 9, 6);
    PROC_INDEX_TERM('rights', 9, 10);

    PROC_INDEX_TERM('lease', 10, 14);
    PROC_INDEX_TERM('tenant', 10, 9);
    PROC_INDEX_TERM('landlord', 10, 8);
    PROC_INDEX_TERM('rent', 10, 11);
    PROC_INDEX_TERM('agreement', 10, 6);
    PROC_INDEX_TERM('property', 10, 7);

    -- Cross-document terms
    PROC_INDEX_TERM('contract', 3, 5);
    PROC_INDEX_TERM('contract', 10, 4);
    PROC_INDEX_TERM('court', 2, 9);
    PROC_INDEX_TERM('court', 9, 5);
    PROC_INDEX_TERM('penalty', 9, 3);
    PROC_INDEX_TERM('regulation', 4, 4);
    PROC_INDEX_TERM('regulation', 8, 3);
END;
/

-- ============================================================
-- 6. QUERY_LOG sample entries
-- ============================================================
INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'contract', 45, SYSDATE - 2);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'rights', 38, SYSDATE - 1);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'constitution', 32, SYSDATE - 3);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'bail', 27, SYSDATE - 1);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'protection', 24, SYSDATE);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'consumer', 19, SYSDATE - 4);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'property', 17, SYSDATE - 2);

INSERT INTO QUERY_LOG (query_id, search_term, search_count, last_searched)
VALUES (SEQ_QUERY_LOG.NEXTVAL, 'amendment', 15, SYSDATE - 5);

COMMIT;

-- ============================================================
-- 7. VERIFICATION QUERIES
-- ============================================================

-- Verify DOCUMENT_TYPE
SELECT * FROM DOCUMENT_TYPE ORDER BY type_id;

-- Verify LANGUAGE
SELECT * FROM LANGUAGE ORDER BY language_id;

-- Verify DOCUMENTS
SELECT doc_id, title, file_name, content_length, category, jurisdiction, created_at
FROM DOCUMENTS ORDER BY doc_id;

-- Verify TERMS
SELECT * FROM TERMS ORDER BY term_id;

-- Verify INVERTED_INDEX
SELECT ii.term_id, t.term_text, ii.doc_id, d.title, ii.frequency
FROM INVERTED_INDEX ii
JOIN TERMS t ON t.term_id = ii.term_id
JOIN DOCUMENTS d ON d.doc_id = ii.doc_id
ORDER BY ii.doc_id, ii.frequency DESC;

-- Verify QUERY_LOG
SELECT * FROM QUERY_LOG ORDER BY search_count DESC;

-- Verify STOPWORDS
SELECT s.stopword_id, s.word, l.language_name
FROM STOPWORDS s
JOIN LANGUAGE l ON l.language_id = s.language_id
ORDER BY s.word;

-- Verify DOCUMENT_STATS
SELECT ds.stat_id, ds.doc_id, d.title, ds.total_terms, ds.unique_terms, ds.last_indexed
FROM DOCUMENT_STATS ds
JOIN DOCUMENTS d ON d.doc_id = ds.doc_id
ORDER BY ds.doc_id;

-- Test PROC_SEARCH_DOCUMENTS
VARIABLE rc REFCURSOR;
EXEC PROC_SEARCH_DOCUMENTS('contract', :rc);
PRINT rc;

-- Test PROC_GET_TOP_TERMS
VARIABLE rc2 REFCURSOR;
EXEC PROC_GET_TOP_TERMS(5, :rc2);
PRINT rc2;

-- Test PROC_GET_DOC_STATS
VARIABLE rc3 REFCURSOR;
EXEC PROC_GET_DOC_STATS(1, :rc3);
PRINT rc3;

SELECT 'All sample data inserted and verified successfully' AS status FROM DUAL;
