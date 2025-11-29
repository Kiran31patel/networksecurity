
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://kiranpatelbpprasanna_db_user:pS0zmDtKp3r1v3ot@cluster0.jmsiagd.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db_name = "NetworkSecurityDB"
    print("Pinged your deployment. You successfully connected to MongoDB!")
    print("Collections in DB:", client[db_name].list_collection_names())
    collection_name = "PhisingDataCollection"
    count = client[db_name][collection_name].count_documents({})
    print(f"Documents in {collection_name}: {count}")
except Exception as e:
    print(e)