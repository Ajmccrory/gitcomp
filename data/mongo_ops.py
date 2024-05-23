from pymongo import MongoClient

URI = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.3'

class MongoOperations:
    """
    MongoDB operations for the GitHub data.

    Attributes:
        client (MongoClient): The MongoDB client.
        db (Database): The MongoDB database.
        collection (Collection): The MongoDB collection for user contributions.
        repo_collection (Collection): The MongoDB collection for user repositories.
    """

    def __init__(self):
        """
        Initializes the MongoDB connection and collections.
        """
        self.client = MongoClient(URI)
        self.db = self.client['git_data']
        self.collection = self.db['user_contributions']
        self.repo_collection = self.db['user_repos']

    def insert_one(self, data):
        """
        Inserts a single document into the user contributions collection.

        Args:
            data (dict): The data to insert, typically containing username and contributions.
        """
        self.collection.insert_one(data)

    def find_one(self, query):
        """
        Finds a single document in the user contributions collection.

        Args:
            query (dict): The query to match, typically containing the username.

        Returns:
            dict: The document found, or None if no document matches the query.
        """
        return self.collection.find_one(query)

    def clear_collection(self, username):
        """
        Deletes all documents for a specific username in the user contributions collection.

        Args:
            username (str): The username whose documents should be deleted.
        """
        self.collection.delete_many({'username': username})

    def close(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
