from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

CONNECTING_STRING = "postgresql://postgres:javokh7778@localhost:5432/crm_db"

class Base(DeclarativeBase):
    pass

engine = create_engine(CONNECTING_STRING)
Session = sessionmaker(bind=engine)