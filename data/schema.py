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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Create index for common queries
    UNIQUE(project_name, snapshot_date, snapshot_time, doc_ref, revision)
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

-- Revision summary table
-- Pre-aggregated revision counts by project and date
CREATE TABLE IF NOT EXISTS revision_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_time TIME NOT NULL,
    revision_type TEXT NOT NULL,  -- 'P01', 'P02', 'C01', etc.
    count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_name, snapshot_date, snapshot_time, revision_type)
);

-- Status summary table
-- Pre-aggregated status counts by project and date
CREATE TABLE IF NOT EXISTS status_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_time TIME NOT NULL,
    status TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_name, snapshot_date, snapshot_time, status)
);

-- File type summary table
-- Pre-aggregated file type counts by project and date
CREATE TABLE IF NOT EXISTS file_type_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_time TIME NOT NULL,
    file_type TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(project_name, snapshot_date, snapshot_time, file_type)
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_documents_project_date 
    ON documents(project_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_documents_status 
    ON documents(status);

CREATE INDEX IF NOT EXISTS idx_documents_revision 
    ON documents(revision);

CREATE INDEX IF NOT EXISTS idx_revision_summaries_project_date 
    ON revision_summaries(project_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_status_summaries_project_date 
    ON status_summaries(project_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_file_type_summaries_project_date 
    ON file_type_summaries(project_name, snapshot_date);
"""

# Version tracking for schema migrations
SCHEMA_VERSION = 1

