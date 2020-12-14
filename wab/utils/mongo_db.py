from pymongo import MongoClient


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class MongoDBManager(object):
    __metaclass__ = Singleton
    hosts = {}

    def connection_mongo(self, host='localhost', port=27017, database=None):
        if host in self.hosts.keys():
            return self.hosts[host]
        else:
            client = MongoClient(host, port, maxPoolSize=50)
            db = client[database]
            self.hosts[host] = db
            return db

    def get_all_collections(self, db):
        collections = db.list_collection_names()
        return collections

    def get_all_documents(self, collection):
        documents = []
        cursor = collection.find({})
        for document in cursor:
            documents.append(document)
        return documents

    def get_one_document(self, collection):
        cursor = collection.find({})
        for document in cursor:
            return document

    def get_all_keys(self, document):
        return document.keys()

    def create_new_collection(self, db, collection_name):
        collection = db[collection_name]
        return collection

    def create_new_field(self, collection, field_name, field_value):
        collection.insert({field_name: field_value})
