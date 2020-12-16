import urllib.parse

from pymongo import MongoClient

from wab.utils.constant import MONGO_SRV_CONNECTION, MONGO_CONNECTION


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
    databases = {}

    def connection_mongo(self, host='localhost', port=None, database=None, prefix=None, username=None, password=None,
                         ssl=False):
        if host in self.hosts.keys() and database in self.databases.keys():
            return self.hosts[host]
        else:
            us = urllib.parse.quote_plus(username)
            pw = urllib.parse.quote_plus(password)
            str_ssl = 'false'
            if ssl:
                str_ssl = 'true'
            if port <= 0:
                prefix = MONGO_SRV_CONNECTION
                client = MongoClient('%s://%s:%s@%s/?ssl=%s' % (prefix, us, pw, host, str_ssl))
            else:
                prefix = MONGO_CONNECTION
                client = MongoClient('%s://%s:%s@%s:%s/?ssl=%s' % (prefix, us, pw, host, str(port), str_ssl))
            # client = MongoClient(host,
            #                      username=username,
            #                      password=password,
            #                      authSource=database,
            #                      authMechanism='SCRAM-SHA-256',
            #                      ssl=ssl)
            db = client[database]
            self.hosts[host] = db
            self.databases[database] = database
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


class PostgresManager(object):
    __metaclass__ = Singleton
    hosts = {}

    def __init__(self):
        pass


class MySQLManager(object):
    __metaclass__ = Singleton
    hosts = {}

    def __init__(self):
        pass
