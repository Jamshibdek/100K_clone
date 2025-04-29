from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
DATABASE_URL = "sqlite:///./test.db"  # test uchun sqlite, productionda PostgreSQL ishlatamiz

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ForeignKey check for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
