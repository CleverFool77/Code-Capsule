# db_creator.py
 
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
engine = create_engine('sqlite:///wmn19.db', echo=True)
Base = declarative_base() 
 
class Codebase(Base):
    """"""
    __tablename__ = "codebase"
 
    id = Column(Integer, primary_key=True)
    date = Column(Date,default=datetime.today().date())
    code_count = Column(Integer)
 
    def __init__(self, date, code_count):
        """"""
        self.date = date
        self.code_count = code_count
 
# create tables
Base.metadata.create_all(engine)