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
                    INSERT INTO documents (
                        project_name, snapshot_date, snapshot_time,
                        doc_ref, doc_title, revision, status, file_type,
                        purpose_of_issue, date_wet, last_status_change_wet,
                        last_updated_wet, doc_path, publisher
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    project_name,
                    snapshot_date,
                    snapshot_time,
                    clean_string(row.get('Doc Ref', '')),
                    clean_string(row.get('Doc Title', '')),
                    clean_string(row.get('Rev', '')),
                    clean_string(row.get('Status', '')),
                    clean_string(row.get('File Type', '')),  # Now expects standardized column from COLUMN_MAPPINGS
                    clean_string(row.get('Purpose of Issue', '')),
                    clean_string(row.get('Date (WET)', '')),
                    clean_string(row.get('Last Status Change (WET)', '')),
                    clean_string(row.get('Last Updated (WET)', '')),
                    clean_string(row.get('Doc Path', '')),
                    clean_string(row.get('Publisher', ''))
                ))
                inserted += 1
            except Exception as e:
                print(f"Error inserting document {row.get('Doc Ref', 'unknown')}: {str(e)}")
                continue
        
        self.conn.commit()
        return inserted
    
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
                   doc_path AS 'Doc Path',
                   publisher AS 'Publisher'
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
    
    def get_documents_for_snapshot(self, project_name, snapshot_date, snapshot_time):
        """Get documents for a specific snapshot.
        
        Args:
            project_name: Name of the project
            snapshot_date: Date in YYYY-MM-DD format
            snapshot_time: Time in HH:MM format
            
        Returns:
            DataFrame: Document data for this snapshot
        """
        query = """
            SELECT doc_ref AS 'Doc Ref',
                   doc_title AS 'Doc Title',
                   revision AS 'Rev',
                   status AS 'Status',
                   file_type AS 'File Type',
                   date_wet AS 'Date (WET)',
                   doc_path AS 'Doc Path',
                   publisher AS 'Publisher'
            FROM documents
            WHERE project_name = ?
              AND snapshot_date = ?
              AND snapshot_time = ?
        """
        
        return pd.read_sql_query(query, self.conn, params=(project_name, snapshot_date, snapshot_time))
    
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
    
    # DEPRECATED: The following functions used old summary tables and are no longer needed
    # All counting is now done dynamically - see analyzers/dynamic_counting.py
    
    def get_monthly_summaries(self, project_name, exclude_current_month=True):
        """Get last snapshot of each completed month.
        
        Args:
            project_name: Name of the project
            exclude_current_month: If True, exclude the current month
            
        Returns:
            DataFrame: Summary data with one row per month (last snapshot)
        """
        # Get all unique months
        query = """
            SELECT DISTINCT 
                strftime('%Y-%m', snapshot_date) as month,
                MAX(snapshot_date) as last_date,
                snapshot_time
            FROM documents
            WHERE project_name = ?
            GROUP BY strftime('%Y-%m', snapshot_date)
            ORDER BY month
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (project_name,))
        months = cursor.fetchall()
        
        if not months:
            return pd.DataFrame()
        
        # If exclude current month, remove the last month
        if exclude_current_month and months:
            current_month = datetime.now().strftime('%Y-%m')
            months = [m for m in months if m[0] != current_month]
        
        # For each month, get the last snapshot's summary data
        monthly_data = []
        
        for month, last_date, _ in months:
            # Get the last snapshot time for this date
            time_query = """
                SELECT snapshot_time
                FROM documents
                WHERE project_name = ? AND snapshot_date = ?
                ORDER BY snapshot_time DESC
                LIMIT 1
            """
            cursor.execute(time_query, (project_name, last_date))
            time_result = cursor.fetchone()
            if not time_result:
                continue
            
            last_time = time_result[0]
            
            # Get summary for this snapshot
            snapshot_data = self._get_snapshot_summary(project_name, last_date, last_time)
            if snapshot_data:
                # Format date as "Month-YYYY" (e.g., "Jun-2025")
                date_obj = datetime.strptime(last_date, '%Y-%m-%d')
                snapshot_data['Date'] = date_obj.strftime('%b-%Y')
                snapshot_data['Time'] = last_time
                snapshot_data['_is_monthly'] = True  # Flag for formatting
                snapshot_data['_snapshot_date'] = last_date  # Store raw date for querying
                snapshot_data['_snapshot_time'] = last_time  # Store raw time for querying
                monthly_data.append(snapshot_data)
        
        return pd.DataFrame(monthly_data)
    
    def get_last_n_weeks(self, project_name, n=4):
        """Get last N weeks of snapshots.
        
        Args:
            project_name: Name of the project
            n: Number of recent weeks to retrieve
            
        Returns:
            DataFrame: Summary data for last N snapshots
        """
        # Get last N snapshots
        query = """
            SELECT DISTINCT snapshot_date, snapshot_time
            FROM documents
            WHERE project_name = ?
            ORDER BY snapshot_date DESC, snapshot_time DESC
            LIMIT ?
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (project_name, n))
        snapshots = cursor.fetchall()
        
        if not snapshots:
            return pd.DataFrame()
        
        # Reverse to get chronological order
        snapshots = list(reversed(snapshots))
        
        # Get summary for each snapshot
        weekly_data = []
        for snapshot_date, snapshot_time in snapshots:
            snapshot_data = self._get_snapshot_summary(project_name, snapshot_date, snapshot_time)
            if snapshot_data:
                # Format date as "DD-Mon-YYYY"
                date_obj = datetime.strptime(snapshot_date, '%Y-%m-%d')
                snapshot_data['Date'] = date_obj.strftime('%d-%b-%Y')
                snapshot_data['Time'] = snapshot_time
                snapshot_data['_is_monthly'] = False  # Flag for formatting
                snapshot_data['_snapshot_date'] = snapshot_date  # Store raw date for querying
                snapshot_data['_snapshot_time'] = snapshot_time  # Store raw time for querying
                weekly_data.append(snapshot_data)
        
        return pd.DataFrame(weekly_data)
    
    def get_condensed_summary(self, project_name, num_recent_weeks=4):
        """Get condensed summary: monthly summaries + last N weeks.
        
        Excludes monthly summaries for months already covered by the last N weeks.
        
        Args:
            project_name: Name of the project
            num_recent_weeks: Number of recent weeks to show in detail
            
        Returns:
            DataFrame: Combined monthly summaries and recent weeks
        """
        # Get last N weeks first
        weekly_df = self.get_last_n_weeks(project_name, num_recent_weeks)
        
        if weekly_df.empty:
            # No recent weeks, just return monthly summaries
            return self.get_monthly_summaries(project_name, exclude_current_month=True)
        
        # Find which months are already covered by the last N weeks
        covered_months = set()
        for _, row in weekly_df.iterrows():
            # Extract month from Date (format: "DD-Mon-YYYY")
            try:
                date_str = row['Date']
                date_obj = datetime.strptime(date_str, '%d-%b-%Y')
                month_key = date_obj.strftime('%Y-%m')
                covered_months.add(month_key)
            except:
                continue
        
        # Get monthly summaries (excluding current month)
        monthly_df = self.get_monthly_summaries(project_name, exclude_current_month=True)
        
        if monthly_df.empty:
            return weekly_df
        
        # Filter out monthly summaries for months already covered by recent weeks
        filtered_monthly = []
        for _, row in monthly_df.iterrows():
            # Extract month from Date (format: "Mon-YYYY")
            try:
                date_str = row['Date']
                # Parse "Jun-2025" format
                date_obj = datetime.strptime(date_str, '%b-%Y')
                month_key = date_obj.strftime('%Y-%m')
                
                # Only include if this month is NOT in the recent weeks
                if month_key not in covered_months:
                    filtered_monthly.append(row)
            except:
                continue
        
        # Combine filtered monthly summaries + recent weeks
        if not filtered_monthly:
            return weekly_df
        
        monthly_filtered_df = pd.DataFrame(filtered_monthly)
        return pd.concat([monthly_filtered_df, weekly_df], ignore_index=True)
    
    def _get_snapshot_summary(self, project_name, snapshot_date, snapshot_time):
        """Get summary data for a specific snapshot.
        
        Args:
            project_name: Name of the project
            snapshot_date: Date in YYYY-MM-DD format
            snapshot_time: Time in HH:MM format
            
        Returns:
            dict: Summary data for this snapshot
        """
        record = {}
        
        # Get revision counts
        rev_query = """
            SELECT revision_type, count
            FROM revision_summaries
            WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(rev_query, (project_name, snapshot_date, snapshot_time))
        for row in cursor.fetchall():
            count_val = int(row[1]) if pd.notna(row[1]) else 0
            record[f"Rev_{row[0]}"] = count_val
        
        # Get status counts
        status_query = """
            SELECT status, count
            FROM status_summaries
            WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
        """
        cursor.execute(status_query, (project_name, snapshot_date, snapshot_time))
        for row in cursor.fetchall():
            count_val = int(row[1]) if pd.notna(row[1]) else 0
            record[f"Status_{row[0]}"] = count_val
        
        # Get file type counts
        ft_query = """
            SELECT file_type, count
            FROM file_type_summaries
            WHERE project_name = ? AND snapshot_date = ? AND snapshot_time = ?
        """
        cursor.execute(ft_query, (project_name, snapshot_date, snapshot_time))
        for row in cursor.fetchall():
            count_val = int(row[1]) if pd.notna(row[1]) else 0
            record[f"FileType_{row[0]}"] = count_val
        
        return record if record else None

