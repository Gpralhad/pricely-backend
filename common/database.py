import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# 2. Updated URL: 
# - Removed ?pgbouncer=true
# - Used port 6543
# - Use +psycopg2 to be explicit
#DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@db.dxqseiyhjkjfxhzgdixc.supabase.co:6543/postgres"

#DATABASE_URL = f"postgresql://postgres.dxqseiyhjkjfxhzgdixc:{password}@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"


# If you are using the manual string construction:
user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
DATABASE_URL = f"postgresql://postgres.{user}:{password}@{host}:6543/postgres"


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