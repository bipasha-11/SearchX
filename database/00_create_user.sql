-- ============================================================
-- SEARCHX: Create Database User (run as SYSDBA)
-- ============================================================

-- For Oracle 21c XE, allow non-CDB style usernames
ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE;

-- Drop user if exists (ignore error if not exists)
BEGIN
    EXECUTE IMMEDIATE 'DROP USER searchx CASCADE';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Create user
CREATE USER searchx IDENTIFIED BY searchx123;

-- Grant privileges
GRANT CONNECT, RESOURCE TO searchx;
GRANT CREATE VIEW, CREATE SEQUENCE, CREATE TRIGGER, CREATE PROCEDURE TO searchx;
GRANT UNLIMITED TABLESPACE TO searchx;

-- Verify
SELECT username, account_status FROM dba_users WHERE username = 'SEARCHX';

EXIT;
