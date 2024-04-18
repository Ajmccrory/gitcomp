from pymongo import MongoClient

URI = 'mongodb://localhost:27017'
class MongoOperations:

    def __init__(self):
        self.client = MongoClient(URI)  # MongoDB connection
        self.db = self.client['git_data']  # MongoDB database
        self.collection = self.db['user_contributions']  # MongoDB collection

    def insert_one(self, data):
        self.collection.insert_one(data)

    def find_one(self, query):
        return self.collection.find_one(query)
    
    def close(self):
        self.client.close()