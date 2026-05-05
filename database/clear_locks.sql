-- Check and kill locked sessions for SEARCHX user
SET LINESIZE 200
SET PAGESIZE 100
COLUMN SID FORMAT 9999
COLUMN SERIAL# FORMAT 99999
COLUMN USERNAME FORMAT A15
COLUMN STATUS FORMAT A10

SELECT s.sid, s.serial#, s.username, s.status 
FROM v$session s 
WHERE s.username = 'SEARCHX';

-- Kill all SEARCHX sessions that might be holding locks
BEGIN
    FOR r IN (SELECT sid, serial# FROM v$session WHERE username = 'SEARCHX') LOOP
        BEGIN
            EXECUTE IMMEDIATE 'ALTER SYSTEM KILL SESSION ''' || r.sid || ',' || r.serial# || ''' IMMEDIATE';
            DBMS_OUTPUT.PUT_LINE('Killed session ' || r.sid || ',' || r.serial#);
        EXCEPTION
            WHEN OTHERS THEN NULL;
        END;
    END LOOP;
END;
/

EXIT;
