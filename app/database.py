from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password} \
@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base create a central class that all of others models inherit from.
Base = declarative_base()

# Dependency Injection to provide database connection to endpoints
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

