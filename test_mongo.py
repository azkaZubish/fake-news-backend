from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://azkazubish_db_user:ZL5ZsIRnVUl6MzAE@cluster0.zklopxo.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1")
)

try:
    client.admin.command("ping")
    print("Connected!")
except Exception as e:
    print(e)