import urllib.parse
from datetime import datetime

import bson.objectid
import pymongo
from pymongo import MongoClient

from wab.core.sql_function.models import SqlFunction, SqlFunctionMerge, SqlFunctionOrderBy, OPERATOR, RELATION
from wab.utils import responses
from wab.utils.constant import MONGO_SRV_CONNECTION, MONGO_CONNECTION
from wab.utils.operator import OPERATOR_MONGODB


def json_mongo_handler(x):
    if isinstance(x, datetime):
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

    def delete_cache_db_exception(self, str_cache_db):
        del self.hosts[str_cache_db]

    def connection_mongo(self, host='localhost', port=None, database=None, username=None, password=None,
                         ssl=False):
        str_cache_db = host
        str_ssl = 'false'
        if ssl:
            str_ssl = 'true'
        str_cache_db = str_cache_db + str_ssl
        if port > 0:
            str_cache_db = str_cache_db + str(port)
        if str_cache_db in self.hosts.keys():
            return self.hosts[str_cache_db], str_cache_db
        else:
            try:
                us = urllib.parse.quote_plus(username)
                pw = urllib.parse.quote_plus(password)
                if port <= 0:
                    prefix = MONGO_SRV_CONNECTION
                    client = MongoClient('%s://%s:%s@%s/?ssl=%s' % (prefix, us, pw, host, str_ssl))
                else:
                    prefix = MONGO_CONNECTION
                    client = MongoClient('%s://%s:%s@%s:%s/?ssl=%s' % (prefix, us, pw, host, str(port), str_ssl))
                db = client[database]
                self.hosts[str_cache_db] = db
                return db, str_cache_db
            except Exception as err:
                raise Exception(err)

    def connection_mongo_by_provider(self, provider_connection=None):
        return self.connection_mongo(host=provider_connection.host,
                                     port=provider_connection.port,
                                     username=provider_connection.username,
                                     password=provider_connection.password,
                                     database=provider_connection.database,
                                     ssl=provider_connection.ssl)

    def get_all_collections(self, db, cache_db=None):
        try:
            collections = db.list_collection_names()
            return collections
        except Exception as err:
            if cache_db:
                self.delete_cache_db_exception(cache_db)
            raise Exception(err)

    def get_all_documents(self, db, collection, column_sort, page=1, page_size=20, sort=pymongo.DESCENDING):
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

    def create_new_field(self, db, collection_name, field_name, field_value):
        collection = db[collection_name]
        collection.insert({field_name: field_value})
        return collection

    def insert_data_collection(self, db, collection_name, list_data):
        collection = db[collection_name]
        collection.insert(list_data)

    @staticmethod
    def export_db_by_column(db, table, list_filter=None, list_column=None):
        collection = db[table]
        if list_column:
            select_column = {}
            for c in list_column:
                select_column.update({c: 1})
            if list_filter:
                return collection.find(
                    list_filter,
                    select_column
                )
            else:
                return collection.find({}, select_column)
        else:
            return collection.find({})

    @staticmethod
    def find_by_fk(db, table, column, condition, value):
        mongo_db_manager = MongoDBManager()
        operator, value = mongo_db_manager.condition_filter(condition, value)
        return db[table].find({
            column: {
                operator: value
            }
        })

    @staticmethod
    def condition_filter(condition, value):
        operator = '$eq'
        if condition == OPERATOR_MONGODB.get_value('operator_equals'):
            operator = '$eq'
        elif condition == OPERATOR_MONGODB.get_value('operator_not_equals'):
            operator = '$ne'
        elif condition == OPERATOR_MONGODB.get_value('operator_less_than'):
            operator = '$lt'
        elif condition == OPERATOR_MONGODB.get_value('operator_less_than_or_equals'):
            operator = '$lte'
        elif condition == OPERATOR_MONGODB.get_value('operator_greater_than'):
            operator = '$gt'
        elif condition == OPERATOR_MONGODB.get_value('operator_greater_than_or_equals'):
            operator = '$gte'
        elif condition == OPERATOR_MONGODB.get_value('operator_in'):
            operator = '$in'
            # value = value.split(',')
        elif condition == OPERATOR_MONGODB.get_value('operator_not_in'):
            operator = '$nin'
            # value = value.split(',')
        elif condition == OPERATOR_MONGODB.get_value('operator_contains'):
            operator = '$regex'
            value = f".*{value}.*"
        return operator, value

    @staticmethod
    def union(db, table_1, field_1, table_2, field_2, condition_items, order_by):
        if order_by is None:
            order_by = field_1
        list_match_and_tb1 = []
        list_match_or_tb1 = []
        list_match_and_tb2 = []
        list_match_or_tb2 = []
        for condition in condition_items:
            if condition.table_name == table_1:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and_tb1.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or_tb1.append(item)
            else:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and_tb2.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or_tb2.append(item)
        pipeline = [
            {"$limit": 1},  # Reduce the result set to a single document.
            {"$project": {"_id": 1}},  # Strip all fields except the Id.
            {"$project": {"_id": 0}},  # Strip the id. The document is now empty.
            {
                "$lookup": {
                    "from": table_1,
                    "pipeline": [
                        {
                            "$match": {
                                "$and": list_match_and_tb1,
                                "$or": list_match_or_tb1
                            }
                        },
                        {
                            "$project": {
                                "_id": 0, "result": "$" + field_1
                            }
                        }
                    ],
                    "as": "collection_table_1"
                }
            },
            {
                "$lookup": {
                    "from": table_2,
                    "pipeline": [
                        {
                            "$match": {
                                "$and": list_match_and_tb2,
                                "$or": list_match_or_tb2
                            }
                        },
                        {
                            "$project": {
                                "_id": 0, "result": "$" + field_2
                            }
                        }
                    ],

                    "as": "collection_table_2"
                }
            },
            {"$project": {
                "union": {"$setUnion": ["$collection_table_1", "$collection_table_2"]}
            }},
            {"$unwind": "$union"},  # Unwind the union collection into a result set.
            {"$replaceRoot": {"newRoot": "$union"}},  # Replace the root to cleanup the resulting documents.
            {"$sort": {order_by: -1}},
        ]
        collection = db[table_1]
        return collection.aggregate(pipeline)

    @staticmethod
    # TODO: right join switch table
    def left_right_join(db, table_1, field_1, table_2, field_2, order_by, condition_items, page, page_size):
        if order_by is None:
            order_by = field_1
        collection = db[table_1]
        list_match_and = []
        list_match_or = []
        for condition in condition_items:
            if condition.table_name == table_1:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or.append(item)
            else:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or.append(item)

        pipeline = [
            {"$skip": page},
            {"$limit": page_size},
            {
                "$lookup": {
                    "from": table_2,
                    "localField": field_1,
                    "foreignField": field_2,
                    "as": "data"
                },
            },
            {"$unwind": "$data"},
            {
                "$match": {
                    "$and": list_match_and,
                    "$or": list_match_or
                }
            },
            {"$sort": {order_by: -1}},
            {
                "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
            },
            {
                "$project": {"data": 0, "_id": 0}
            }
        ]
        return collection.aggregate(pipeline)

    @staticmethod
    def inner_join(db, table_1, field_1, table_2, field_2, order_by, condition_items, page, page_size):
        if order_by is None:
            order_by = field_1
        collection = db[table_1]
        list_match_and = []
        list_match_or = []
        for condition in condition_items:
            if condition.table_name == table_1:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_equal'):
                        item = {condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or.append(item)
            else:
                if condition.relation is None or condition.relation == RELATION.get_value('relation_and'):
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_and.append(item)
                else:
                    if condition.operator == OPERATOR.get_value('type_equal'):
                        item = {"data." + condition.field_name: {"$eq": condition.value}}
                    elif condition.operator == OPERATOR.get_value('type_in'):
                        item = {"data." + condition.field_name: {"$in": [condition.value]}}
                    else:
                        item = {"data." + condition.field_name: {"$regex": ".*" + condition.value + ".*"}}
                    list_match_or.append(item)

        pipeline = [
            {"$skip": page},
            {"$limit": page_size},
            {
                "$lookup": {
                    "from": table_2,
                    "localField": field_1,
                    "foreignField": field_2,
                    "as": "data"
                },
            },
            {
                "$unwind":
                    {
                        "path": "$data",
                        "preserveNullAndEmptyArrays": False
                    }
            },
            {
                "$match": {
                    "$and": list_match_and,
                    "$or": list_match_or
                }
            },
            {"$sort": {order_by: -1}},
            {
                "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
            },
            {
                "$project": {"data": 0, "_id": 0}
            }
        ]
        return collection.aggregate(pipeline)

    def sql_function_exe(self, collection_name, sql_function_id):
        try:
            sql_function = SqlFunction.objects.get(id=sql_function_id)
            db = self.connection_mongo_by_provider(sql_function.provider)
            collection = db[collection_name]
            sql_function_merge = SqlFunctionMerge.objects.filter(sql_function=sql_function)
            if len(sql_function_merge):
                for index, merge in enumerate(sql_function_merge):
                    table_name_first = merge.table_name
                    merge_type = merge.merge_type
                    if merge_type:
                        merge_after = sql_function_merge[index + 1]
                        table_name_second = merge_after.table_name
                        self.left_join()

                order_bys = SqlFunctionOrderBy.objects.filter(sql_function=sql_function)
            else:
                return responses.bad_request(data='SQL error', message_code='MERGE_TYPE_ERROR')
        except Exception as err:
            return responses.bad_request(data='SQL error', message_code='SQL_ERROR', )


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
