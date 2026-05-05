SET PAGESIZE 50
COLUMN username FORMAT A20
COLUMN email FORMAT A30
COLUMN full_name FORMAT A20
SELECT user_id, username, email, full_name, created_at FROM USERS;
EXIT;
