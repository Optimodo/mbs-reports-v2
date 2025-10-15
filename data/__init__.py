"""Data storage and database operations module."""

from .database import DocumentDatabase
from .schema import DATABASE_SCHEMA, SCHEMA_VERSION

__all__ = [
    'DocumentDatabase',
    'DATABASE_SCHEMA',
    'SCHEMA_VERSION'
]

