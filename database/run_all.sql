-- ============================================================
-- SEARCHX: Master DB Setup Script
-- Runs: 01_schema.sql → 02_sample_data.sql → 03_auth_schema.sql
-- ============================================================
WHENEVER SQLERROR CONTINUE
SET ECHO OFF
SET FEEDBACK ON
SET PAGESIZE 50
SET LINESIZE 120

PROMPT ============================================================
PROMPT STEP 1: Creating Schema (Tables, Sequences, Triggers, Procs)
PROMPT ============================================================
@D:\SEARCHX\database\01_schema.sql

PROMPT ============================================================
PROMPT STEP 2: Inserting Sample Data
PROMPT ============================================================
@D:\SEARCHX\database\02_sample_data.sql

PROMPT ============================================================
PROMPT STEP 3: Auth Schema (USERS table + procedure)
PROMPT ============================================================
@D:\SEARCHX\database\03_auth_schema.sql

PROMPT ============================================================
PROMPT ALL DONE - Database is ready!
PROMPT ============================================================

EXIT;
