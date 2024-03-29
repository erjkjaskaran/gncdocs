import pymongo


class Database(object):
    URI = f'mongodb+srv://root:root@cluster0.4fnhrtj.mongodb.net/?retryWrites=true&w=majority'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["dbgncdocs"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_one(collection, query):
        Database.DATABASE[collection].delete_one(query)
