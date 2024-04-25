from pymongo import MongoClient

URI = 'mongodb://localhost:27017'
class MongoOperations:
    """
    create monogdb object
    :param:
    :return:
    """

    def __init__(self):
        """
        create mongodb object
        """
        self.client = MongoClient(URI)  # MongoDB connection
        self.db = self.client['git_data']  # MongoDB database
        self.collection = self.db['user_contributions']  # MongoDB collection
        self.repo_collection = self.db['user_repos']

    def insert_one(self, data):
        """
        insert data in db
        :param data: data object containing username and contributions (any)
        :return:
        """
        self.collection.insert_one(data)

    def find_one(self, query):
        """
        pull specific data from db collection
        :param query: username given to find (dict)
        :return (MongoOperations): data object stored in db
        """
        return self.collection.find_one(query)
    
    def close(self):
        self.client.close()

    def clear_collection(self):
        """
        delete all documents in the collection
        """
        cleared = self.collection.delete_many({})
        return cleared.deleted_count