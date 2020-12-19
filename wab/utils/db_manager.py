import urllib.parse
import pymongo
from pymongo import MongoClient
import datetime
import bson.objectid
from wab.utils.constant import MONGO_SRV_CONNECTION, MONGO_CONNECTION


def json_mongo_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)


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

    def connection_mongo_by_provider(self, provider_connection=None):
        return self.connection_mongo(host=provider_connection.host,
                                     port=provider_connection.port,
                                     username=provider_connection.username,
                                     password=provider_connection.password,
                                     database=provider_connection.database,
                                     ssl=provider_connection.ssl)

    def get_all_collections(self, db):
        collections = db.list_collection_names()
        return collections

    def get_all_documents(self, db, collection, column_sort, page, page_size, sort=pymongo.DESCENDING):
        if column_sort:
            documents = db[collection].find({}).sort(column_sort, sort).skip((page - 1) * page_size).limit(page_size)
        else:
            documents = db[collection].find({}).skip((page - 1) * page_size).limit(page_size)
        count = documents.count()
        return documents, count

    def get_all_keys(self, db, collection):
        cursor = db[collection].find({})
        for document in cursor:
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
