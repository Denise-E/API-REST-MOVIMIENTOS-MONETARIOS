from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://DESKTOP-BKKMKDA\denue:@DESKTOP-BKKMKDA\MSSQLSERVER01/banza"
# https://fastapi.tiangolo.com/tutorial/sql-databases/ A CHEQUEAR CONFIG

engine = create_engine( SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
