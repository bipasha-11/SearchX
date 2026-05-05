SET PAGESIZE 50
SET LINESIZE 200
COLUMN column_name FORMAT A20
COLUMN data_type FORMAT A15
SELECT column_name, data_type, data_length FROM user_tab_columns WHERE table_name = 'USERS';
SELECT username, LENGTH(password_hash) as hash_len, password_hash FROM USERS;
EXIT;
