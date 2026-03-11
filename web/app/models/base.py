"""
SQLAlchemy Declarative Base.

This module provides the foundation for all database models. 
By inheriting from this 'Base', models are automatically registered 
with the SQLAlchemy metadata, allowing for centralized schema 
generation and Alembic migrations.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass