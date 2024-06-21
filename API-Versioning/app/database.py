from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#create a SQLite engine and session
engine = create_engine('sqlite:///inventory.db')

#creatae SessionLocal class from Sessionmaker factory
SessionLocal = sessionmaker(bind=engine,
                            expire_on_commit=False)

#create a Declaraive instance
Base = declarative_base()