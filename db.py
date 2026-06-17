from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['fake_news_db']
predictions_collection = db['predictions']

