-- ============================================================
-- SEARCHX: Authentication Schema Extension
-- Adds USERS table and links DOCUMENTS to user ownership
-- ============================================================

-- 1. SEQUENCE
BEGIN
    FOR r IN (SELECT sequence_name FROM user_sequences WHERE sequence_name = 'SEQ_USER') LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || r.sequence_name;
    END LOOP;
END;
/

CREATE SEQUENCE SEQ_USER START WITH 1 INCREMENT BY 1 NOCACHE;

-- 2. USERS TABLE
BEGIN
    FOR r IN (SELECT table_name FROM user_tables WHERE table_name = 'USERS') LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || r.table_name || ' CASCADE CONSTRAINTS';
    END LOOP;
END;
/

CREATE TABLE USERS (
    user_id       NUMBER        PRIMARY KEY,
    username      VARCHAR2(100) NOT NULL UNIQUE,
    email         VARCHAR2(255) NOT NULL UNIQUE,
    password_hash VARCHAR2(500) NOT NULL,
    full_name     VARCHAR2(200) NOT NULL,
    created_at    DATE          DEFAULT SYSDATE NOT NULL
);

-- 3. Auto-generate USER ID
CREATE OR REPLACE TRIGGER trg_user_id
BEFORE INSERT ON USERS
FOR EACH ROW
BEGIN
    IF :NEW.user_id IS NULL THEN
        SELECT SEQ_USER.NEXTVAL INTO :NEW.user_id FROM DUAL;
    END IF;
END;
/

-- 4. INDEX on USERS
CREATE INDEX idx_users_username ON USERS(username);
CREATE INDEX idx_users_email    ON USERS(email);

-- 5. Add OWNER_ID to DOCUMENTS (nullable for backward compatibility)
-- Check if column exists first
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM user_tab_columns
    WHERE table_name = 'DOCUMENTS' AND column_name = 'OWNER_ID';

    IF v_count = 0 THEN
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD (owner_id NUMBER)';
        EXECUTE IMMEDIATE 'ALTER TABLE DOCUMENTS ADD CONSTRAINT fk_doc_owner FOREIGN KEY (owner_id) REFERENCES USERS(user_id)';
        EXECUTE IMMEDIATE 'CREATE INDEX idx_docs_owner ON DOCUMENTS(owner_id)';
    END IF;
END;
/

-- 6. STORED PROCEDURE: Register User
CREATE OR REPLACE PROCEDURE PROC_REGISTER_USER (
    p_username      IN  VARCHAR2,
    p_email         IN  VARCHAR2,
    p_password_hash IN  VARCHAR2,
    p_full_name     IN  VARCHAR2,
    p_user_id       OUT NUMBER
) AS
BEGIN
    SELECT SEQ_USER.NEXTVAL INTO p_user_id FROM DUAL;

    INSERT INTO USERS (user_id, username, email, password_hash, full_name, created_at)
    VALUES (p_user_id, p_username, p_email, p_password_hash, p_full_name, SYSDATE);

    COMMIT;
END;
/

-- Verification
SELECT 'Auth schema created successfully' AS status FROM DUAL;
