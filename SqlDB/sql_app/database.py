from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQL_ALCHEMY_DATABASE_URL ="postgresql://postgres:postgres@localhost/postgres"
# SQL_ALCHEMY_MSSQLSERVER_DATABASE_URL = "mssql+pyodbc://sa:123456@localhost/test?driver=ODBC+Driver+17+for+SQL+Server"

#create the SQLALCHEMY engine
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
