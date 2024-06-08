from sqlalchemy import create_engine, Column, String, Integer, Boolean ,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://quickassistdb_e8yi_user:GIj8c92qF31H7Y6KJPdqH8dyPN9jjrz8@dpg-cpi53luct0pc73fmg5c0-a.oregon-postgres.render.com/quickassistdb_e8yi', echo=True)

Base = declarative_base()



class User(Base):
    __tablename__ = 'responders_login_info'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(80))
    
class User2(Base):
    __tablename__ = 'login_info'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(80))
    ip_address = Column(String)
    sus = Column(Boolean)

class User3(Base):
    __tablename__ = 'reference_number'

    number = Column(Integer, primary_key=True)
    user_called = Column(String(80))
    
class User4(Base):
    __tablename__ = 'location_and_emergency'

    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    emergency = Column(String)
    level = Column(Integer)
    user = Column(String)
    
    
class User5(Base):
    __tablename__ = 'phone_numbers'

    
    id = Column(Integer, primary_key=True)
    number = Column(String)
    where = Column(String)
    



Base.metadata.create_all(engine)

'''
Session = sessionmaker(bind=engine)
session = Session()

new_reference_number = User3(number='QA-1')

session.add(new_reference_number)

session.commit()

session.close()
'''


