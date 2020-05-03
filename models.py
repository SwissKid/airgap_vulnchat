from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message = Column(String)
    timestamp = Column(Integer)


from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)