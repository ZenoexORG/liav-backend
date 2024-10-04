from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv('.env')

uri = os.getenv('MONGO_URI')

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.liavDB

users_collection = db['users']
products_collection = db['products']
providers_collection = db['providers']
customers_collection = db['customers']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)
