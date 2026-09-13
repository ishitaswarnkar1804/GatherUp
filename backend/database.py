import os
import ssl

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Ishiisha1803@localhost:3306/gatherup"
)

connect_args = {}

if "aivencloud.com" in DATABASE_URL:
    connect_args = {
        "ssl": {
            "check_hostname": False,
            "verify_mode": ssl.CERT_NONE
        }
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()