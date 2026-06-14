from dotenv import load_dotenv
import os

load_dotenv()

class Config ():
    db = os.getenv('db')

