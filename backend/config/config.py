import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    