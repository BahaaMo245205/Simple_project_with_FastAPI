from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Backend_App.model import Base
from config import Config

engine = create_engine(Config.db)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()



