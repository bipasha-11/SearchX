SET PAGESIZE 50
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT COUNT(*) AS doc_count FROM documents;
SELECT COUNT(*) AS term_count FROM terms;
SELECT COUNT(*) AS stopword_count FROM stopwords;
EXIT;
