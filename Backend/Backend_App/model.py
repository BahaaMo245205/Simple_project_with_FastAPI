from sqlalchemy import create_engine, ForeignKey, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()


def genrate_uuid():
    return str(uuid.uuid6())


class User(Base):
    __tablename__ = "user"

    UserId = Column( String(100), primary_key=True, default=genrate_uuid)
    UserName = Column( String(100))
    Email = Column(String(100))
    password = Column(String(100))
    
    def __init__ (self,username,email,password):
        self.UserName = username
        self.Email = email
        self.password = password
    
