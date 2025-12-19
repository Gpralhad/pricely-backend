# import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Replace with your actual connection string from Supabase
# # Format: postgresql://postgres:[PASSWORD]@[HOST]:6543/postgres?pgbouncer=true
# #DATABASE_URL = "postgresql://postgres:Vedant786!@db.dxqseiyhjkjfxhzgdixc.supabase.co:5432/postgres?pgbouncer=true"
# # 1. URL-encode the '!' in your password as '%21'
# # 2. Use port 6543 for the transaction pooler
# # 3. Explicitly add +psycopg2 and disable prepared statements
# DATABASE_URL = "postgresql+psycopg2://postgres:Vedant786%21@db.dxqseiyhjkjfxhzgdixc.supabase.co:6543/postgres?pgbouncer=true&prepared_statements=false"

# # Database engine and session setup
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Properly encode your password (handles the '!' character)
password = quote_plus("Vedant786!")

# 2. Updated URL: 
# - Removed ?pgbouncer=true
# - Used port 6543
# - Use +psycopg2 to be explicit
#DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@db.dxqseiyhjkjfxhzgdixc.supabase.co:6543/postgres"

DATABASE_URL = f"postgresql://postgres.dxqseiyhjkjfxhzgdixc:{password}@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"



# 3. Create engine with "prepared statements" disabled
# Supabase pooler (pgbouncer) doesn't support them.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # Verifies connection is alive before using it
    connect_args={
        "prepare_threshold": None  # This disables prepared statements for psycopg2
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()