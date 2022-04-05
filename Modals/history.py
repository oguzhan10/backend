from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:123456@localhost:5432/data-db',echo=False)
Session = sessionmaker(bind=engine)
Session = Session()


Base = declarative_base()

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    event = Column(String)
    messageid = Column(String)
    userid = Column(String)
    properties = Column(String)
    context = Column(String)
    clicked_date = Column(String)


Base.metadata.create_all(engine)