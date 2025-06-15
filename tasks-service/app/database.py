from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
import os

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:asdasd1212@host.docker.internal:5432/To-Do-DB")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:asdasd1212@localhost:5432/To-Do-DB")

engine = create_engine(DATABASE_URL,echo=True)
sessionFactory= Session(engine)
Base = declarative_base()

def get_session():
    try:
        yield sessionFactory
    finally:
        sessionFactory.close()
