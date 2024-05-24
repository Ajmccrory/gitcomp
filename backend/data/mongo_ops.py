from pymongo import MongoClient
import gridfs
from bson import ObjectId

URI = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.3'


class MongoOperations:
    """
    MongoDB operations for the GitHub data.

    Attributes:
        client (MongoClient): The MongoDB client.
        db (Database): The MongoDB database.
        collection (Collection): The MongoDB collection for user contributions.
        repo_collection (Collection): The MongoDB collection for user repositories.
        fs (GridFS): The GridFS instance for handling file storage.
    """

    def __init__(self):
        """
        Initializes the MongoDB connection and collections.
        """
        self.client = MongoClient(URI)
        self.db = self.client['git_data']
        self.collection = self.db['user_contributions']
        self.repo_collection = self.db['user_repos']
        self.fs = gridfs.GridFS(self.db)

    def insert_one(self, data):
        """
        Inserts a document into the user contributions collection.

        :param data: The data object containing username and contributions.
        """
        self.collection.insert_one(data)

    def find_one(self, query):
        """
        Finds a document in the user contributions collection.

        :param query: The query to match.
        :return: The document found, or None if no document matches.
        """
        return self.collection.find_one(query)

    def save_image(self, image_data, filename):
        """
        Saves an image to the database using GridFS.

        :param image_data: The image data to save.
        :return: The ID of the saved image.
        """
        return self.fs.put(image_data, filename=filename)

    def get_image(self, file_id):
        """
        Retrieves an image from the database using GridFS.

        :param file_id: The ID of the file to retrieve.
        :return: The image data.
        """
        file_doc = self.fs.find_one({'_id': ObjectId(file_id)})
        return file_doc

    def close(self):
        """
        Closes the MongoDB client connection.
        """
        self.client.close()

    def clear_collection(self, username):
        """
        Deletes all documents in the collection for a specific user.

        :param username: The username to clear.
        """
        self.collection.delete_many({'username': username})
