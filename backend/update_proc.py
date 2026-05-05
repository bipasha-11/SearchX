from db import get_connection

def update_procedure():
    conn = get_connection()
    cursor = conn.cursor()
    
    procedure_sql = """
    CREATE OR REPLACE PROCEDURE PROC_ADD_DOCUMENT (
        p_title        IN  VARCHAR2,
        p_file_name    IN  VARCHAR2,
        p_content_len  IN  NUMBER,
        p_type_id      IN  NUMBER,
        p_language_id  IN  NUMBER,
        p_category     IN  VARCHAR2,
        p_jurisdiction IN  VARCHAR2,
        p_summary      IN  VARCHAR2,
        p_doc_id       OUT NUMBER
    ) AS
    BEGIN
        SELECT SEQ_DOCUMENT.NEXTVAL INTO p_doc_id FROM DUAL;

        INSERT INTO DOCUMENTS (doc_id, title, file_name, content_length, created_at, type_id, language_id, category, jurisdiction, summary)
        VALUES (p_doc_id, p_title, p_file_name, p_content_len, SYSDATE, p_type_id, p_language_id, p_category, p_jurisdiction, p_summary);

        INSERT INTO DOCUMENT_STATS (doc_id, total_terms, unique_terms, last_indexed)
        VALUES (p_doc_id, 0, 0, NULL);

        COMMIT;
    END;
    """
    
    cursor.execute(procedure_sql)
    conn.commit()
    print("PROC_ADD_DOCUMENT updated successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    update_procedure()
