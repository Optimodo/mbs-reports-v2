"""Database operations for document tracking."""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from .schema import DATABASE_SCHEMA, SCHEMA_VERSION


class DocumentDatabase:
    """SQLite database manager for document tracking."""
    
    def __init__(self, db_path='data/documents.db'):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def initialize_schema(self):
        """Create database schema if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.executescript(DATABASE_SCHEMA)
        self.conn.commit()
        print(f"Database schema initialized at {self.db_path}")
    
    def wipe_database(self):
        """Wipe all data from the database (keeps schema)."""
        cursor = self.conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Delete data from each table
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"DELETE FROM {table_name}")
                print(f"Wiped table: {table_name}")
        
        self.conn.commit()
        print("Database wiped successfully")
    
    def rebuild_database(self):
        """Drop all tables and rebuild schema."""
        cursor = self.conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Drop each table (skip sqlite internal tables)
        for table in tables:
            table_name = table[0]
            # Skip SQLite internal tables
            if table_name.startswith('sqlite_'):
                continue
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Dropped table: {table_name}")
        
        # Drop all indices
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
        indices = cursor.fetchall()
        for index in indices:
            index_name = index[0]
            cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
        
        self.conn.commit()
        
        # Recreate schema
        self.initialize_schema()
        print("Database rebuilt successfully")
    
    def insert_documents(self, project_name, snapshot_date, snapshot_time, documents_df):
        """Insert document records into database.
        
        Args:
            project_name: Name of the project
            snapshot_date: Date of the snapshot (YYYY-MM-DD)
            snapshot_time: Time of the snapshot (HH:MM)
            documents_df: DataFrame containing document data
            
        Returns:
            int: Number of documents inserted
        """
        cursor = self.conn.cursor()
        inserted = 0
        
        for _, row in documents_df.iterrows():
            try:
                # Helper function to clean strings and handle encoding issues
                def clean_string(value):
                    if pd.isna(value) or value == 'nan':
                        return ''
                    s = str(value)
                    # Replace common problematic characters
                    s = s.encode('utf-8', errors='ignore').decode('utf-8')
                    return s
                
                cursor.execute("""
                    INSERT OR REPLACE INTO documents (
                        project_name, snapshot_date, snapshot_time,
                        doc_ref, doc_title, revision, status, file_type,
                        purpose_of_issue, date_wet, last_status_change_wet,
                        last_updated_wet, doc_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project_name,
                    snapshot_date,
                    snapshot_time,
                    clean_string(row.get('Doc Ref', '')),
                    clean_string(row.get('Doc Title', '')),
                    clean_string(row.get('Rev', '')),
                    clean_string(row.get('Status', '')),
                    clean_string(row.get('File Type') or row.get('OVL - File Type') or row.get('Form', '')),
                    clean_string(row.get('Purpose of Issue', '')),
                    clean_string(row.get('Date (WET)', '')),
                    clean_string(row.get('Last Status Change (WET)', '')),
                    clean_string(row.get('Last Updated (WET)', '')),
                    clean_string(row.get('Doc Path', ''))
                ))
                inserted += 1
            except Exception as e:
                print(f"Error inserting document {row.get('Doc Ref', 'unknown')}: {str(e)}")
                continue
        
        self.conn.commit()
        return inserted
    
    def insert_summaries(self, project_name, snapshot_date, snapshot_time, counts):
        """Insert pre-aggregated summary counts.
        
        Args:
            project_name: Name of the project
            snapshot_date: Date of the snapshot
            snapshot_time: Time of the snapshot
            counts: Dictionary of counts (from analyzers.get_counts)
        """
        cursor = self.conn.cursor()
        
        # Insert revision summaries
        for key, count in counts.items():
            # Ensure count is always an integer
            count_int = int(count) if pd.notna(count) and str(count).replace('.', '').replace('-', '').isdigit() else 0
            
            if key.startswith('Rev_'):
                revision_type = key.replace('Rev_', '')
                cursor.execute("""
                    INSERT OR REPLACE INTO revision_summaries
                    (project_name, snapshot_date, snapshot_time, revision_type, count)
                    VALUES (?, ?, ?, ?, ?)
                """, (project_name, snapshot_date, snapshot_time, revision_type, count_int))
            
            # Insert status summaries
            elif key.startswith('Status_'):
                status = key.replace('Status_', '')
                cursor.execute("""
                    INSERT OR REPLACE INTO status_summaries
                    (project_name, snapshot_date, snapshot_time, status, count)
                    VALUES (?, ?, ?, ?, ?)
                """, (project_name, snapshot_date, snapshot_time, status, count_int))
            
            # Insert file type summaries
            elif key.startswith('FileType_'):
                file_type = key.replace('FileType_', '')
                cursor.execute("""
                    INSERT OR REPLACE INTO file_type_summaries
                    (project_name, snapshot_date, snapshot_time, file_type, count)
                    VALUES (?, ?, ?, ?, ?)
                """, (project_name, snapshot_date, snapshot_time, file_type, count_int))
        
        self.conn.commit()
    
    def mark_file_processed(self, project_name, file_path, file_name, snapshot_date, snapshot_time, record_count):
        """Mark a file as processed.
        
        Args:
            project_name: Name of the project
            file_path: Full path to the file
            file_name: Name of the file
            snapshot_date: Date from the file
            snapshot_time: Time from the file
            record_count: Number of records processed
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO processing_history
            (project_name, file_path, file_name, snapshot_date, snapshot_time, record_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (project_name, str(file_path), file_name, snapshot_date, snapshot_time, record_count))
        self.conn.commit()
    
    def is_file_processed(self, project_name, file_name):
        """Check if a file has been processed.
        
        Args:
            project_name: Name of the project
            file_name: Name of the file
            
        Returns:
            bool: True if file has been processed
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM processing_history
            WHERE project_name = ? AND file_name = ?
        """, (project_name, file_name))
        result = cursor.fetchone()
        return result[0] > 0
    
    def get_summary_dataframe(self, project_name):
        """Get summary data as DataFrame for report generation.
        
        Args:
            project_name: Name of the project
            
        Returns:
            DataFrame: Summary data with Date, Time, and all counts
        """
        # Get all unique snapshot dates for this project
        query = """
            SELECT DISTINCT snapshot_date, snapshot_time
            FROM documents
            WHERE project_name = ?
            ORDER BY snapshot_date, snapshot_time
        """
        
        df_dates = pd.read_sql_query(query, self.conn, params=(project_name,))
        
        if df_dates.empty:
            return pd.DataFrame()
        
        summary_data = []
        
        for _, row in df_dates.iterrows():
            snapshot_date = row['snapshot_date']
            snapshot_time = row['snapshot_time']
            
            # Convert date format
            date_obj = datetime.strptime(snapshot_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d-%b-%Y')
            
            record = {
                'Date': formatted_date,
                'Time': snapshot_time
            }
            
            # Get revision counts
            rev_query = """
                SELECT revision_type, count
                FROM revision_summaries
                WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
            """
            rev_df = pd.read_sql_query(rev_query, self.conn, 
                                       params=(project_name, snapshot_date, snapshot_time))
            for _, rev_row in rev_df.iterrows():
                # Ensure count is integer, not string
                count_val = int(rev_row['count']) if pd.notna(rev_row['count']) else 0
                record[f"Rev_{rev_row['revision_type']}"] = count_val
            
            # Get status counts
            status_query = """
                SELECT status, count
                FROM status_summaries
                WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
            """
            status_df = pd.read_sql_query(status_query, self.conn,
                                          params=(project_name, snapshot_date, snapshot_time))
            for _, status_row in status_df.iterrows():
                # Ensure count is integer, not string
                count_val = int(status_row['count']) if pd.notna(status_row['count']) else 0
                record[f"Status_{status_row['status']}"] = count_val
            
            # Get file type counts
            ft_query = """
                SELECT file_type, count
                FROM file_type_summaries
                WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
            """
            ft_df = pd.read_sql_query(ft_query, self.conn,
                                      params=(project_name, snapshot_date, snapshot_time))
            for _, ft_row in ft_df.iterrows():
                # Ensure count is integer, not string
                count_val = int(ft_row['count']) if pd.notna(ft_row['count']) else 0
                record[f"FileType_{ft_row['file_type']}"] = count_val
            
            summary_data.append(record)
        
        return pd.DataFrame(summary_data)
    
    def get_latest_documents(self, project_name):
        """Get the most recent document snapshot for a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            DataFrame: Latest document data
        """
        query = """
            SELECT doc_ref AS 'Doc Ref',
                   doc_title AS 'Doc Title',
                   revision AS 'Rev',
                   status AS 'Status',
                   file_type AS 'File Type',
                   date_wet AS 'Date (WET)',
                   doc_path AS 'Doc Path'
            FROM documents
            WHERE project_name = ?
              AND (snapshot_date, snapshot_time) = (
                  SELECT snapshot_date, snapshot_time
                  FROM documents
                  WHERE project_name = ?
                  ORDER BY snapshot_date DESC, snapshot_time DESC
                  LIMIT 1
              )
        """
        
        return pd.read_sql_query(query, self.conn, params=(project_name, project_name))
    
    def get_project_stats(self, project_name):
        """Get statistics for a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            dict: Project statistics
        """
        cursor = self.conn.cursor()
        
        # Total snapshots
        cursor.execute("""
            SELECT COUNT(DISTINCT snapshot_date || ' ' || snapshot_time)
            FROM documents
            WHERE project_name = ?
        """, (project_name,))
        total_snapshots = cursor.fetchone()[0]
        
        # Total documents in latest snapshot
        cursor.execute("""
            SELECT COUNT(*)
            FROM documents
            WHERE project_name = ?
              AND (snapshot_date, snapshot_time) = (
                  SELECT snapshot_date, snapshot_time
                  FROM documents
                  WHERE project_name = ?
                  ORDER BY snapshot_date DESC, snapshot_time DESC
                  LIMIT 1
              )
        """, (project_name, project_name))
        latest_doc_count = cursor.fetchone()[0]
        
        # Date range
        cursor.execute("""
            SELECT MIN(snapshot_date), MAX(snapshot_date)
            FROM documents
            WHERE project_name = ?
        """, (project_name,))
        date_range = cursor.fetchone()
        
        return {
            'total_snapshots': total_snapshots,
            'latest_document_count': latest_doc_count,
            'first_snapshot': date_range[0],
            'last_snapshot': date_range[1]
        }
    
    def get_all_projects(self):
        """Get list of all projects in the database.
        
        Returns:
            list: Project names
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT project_name FROM documents ORDER BY project_name")
        return [row[0] for row in cursor.fetchall()]

