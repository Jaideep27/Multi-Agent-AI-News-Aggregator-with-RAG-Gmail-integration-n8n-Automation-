"""
Setup script to create the PostgreSQL database if it doesn't exist.
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv('.env')

# Database configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'ai_news_aggregator')

def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect to default 'postgres' database
        print(f"Connecting to PostgreSQL at {POSTGRES_HOST}:{POSTGRES_PORT}...")
        conn = psycopg2.connect(
            dbname='postgres',
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )

        # Set autocommit mode
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (POSTGRES_DB,)
        )
        exists = cursor.fetchone()

        if exists:
            print(f"[OK] Database '{POSTGRES_DB}' already exists")
        else:
            # Create database
            cursor.execute(f'CREATE DATABASE {POSTGRES_DB}')
            print(f"[OK] Database '{POSTGRES_DB}' created successfully")

        cursor.close()
        conn.close()

        return True

    except psycopg2.OperationalError as e:
        print(f"[ERROR] Failed to connect to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("  1. PostgreSQL is running")
        print("  2. Credentials in .env are correct")
        print("  3. PostgreSQL is accessible on localhost:5432")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def create_tables():
    """Create database tables."""
    try:
        print(f"\nCreating tables in '{POSTGRES_DB}'...")
        from src.database.models import Base
        from src.database.connection import engine

        Base.metadata.create_all(engine)
        print("[OK] Tables created successfully")

        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables: {', '.join(tables)}")

        return True
    except Exception as e:
        print(f"[ERROR] Failed to create tables: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AI News Aggregator - Database Setup")
    print("=" * 60)

    # Step 1: Create database
    if create_database():
        # Step 2: Create tables
        if create_tables():
            print("\n" + "=" * 60)
            print("[SUCCESS] Database setup complete!")
            print("=" * 60)
            print("\nYou can now run:")
            print("  python cli.py run")
        else:
            print("\n[ERROR] Table creation failed")
    else:
        print("\n[ERROR] Database creation failed")
