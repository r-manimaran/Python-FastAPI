from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

connection_uri = os.getenv("MONGODB_URI")
print(connection_uri)
#create the client and connect to the server
client = MongoClient(connection_uri, server_api=ServerApi('1'))
db = client.Blogging
blog_collection = db["blogs"]

#send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("exception while connecting")
    print(e)