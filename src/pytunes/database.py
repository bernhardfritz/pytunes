import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import models

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD', '')}@db/pytunes"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
