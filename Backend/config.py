from dotenv import load_dotenv
import os

load_dotenv()

class Config ():
    db = os.getenv('db')
    mysql_password = os.getenv('MySQL_Password')

