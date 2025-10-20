"""Database schema definitions for document tracking."""

# SQLite database schema
DATABASE_SCHEMA = """
-- Document snapshots table
-- Stores one record per document per snapshot date
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_time TIME NOT NULL,
    doc_ref TEXT NOT NULL,
    doc_title TEXT,
    revision TEXT,
    status TEXT,
    file_type TEXT,
    purpose_of_issue TEXT,
    date_wet TEXT,
    last_status_change_wet TEXT,
    last_updated_wet TEXT,
    doc_path TEXT,
    publisher TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    -- No UNIQUE constraint - allow all rows from source files
    -- Database should faithfully represent source data including duplicates
);

-- Processing history table
-- Tracks which files have been processed
CREATE TABLE IF NOT EXISTS processing_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_time TIME NOT NULL,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_count INTEGER,
    
    UNIQUE(project_name, file_name)
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_documents_project_date 
    ON documents(project_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_documents_status 
    ON documents(status);

CREATE INDEX IF NOT EXISTS idx_documents_revision 
    ON documents(revision);

CREATE INDEX IF NOT EXISTS idx_documents_file_type 
    ON documents(file_type);
"""

# Version tracking for schema migrations
SCHEMA_VERSION = 3  # Removed summary tables - fully dynamic counting system

