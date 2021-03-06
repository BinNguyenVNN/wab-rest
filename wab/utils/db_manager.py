import urllib.parse
from datetime import datetime

import bson.objectid
import pymongo
from pymongo import MongoClient, UpdateOne

from wab.core.custom_column.models import CustomColumnTaskConvert
from wab.core.sql_function.models import SqlFunctionMerge, SqlFunctionOrderBy, Relation, MergeType, \
    SqlFunctionConditionItems
from wab.utils.constant import MONGO_SRV_CONNECTION, MONGO_CONNECTION
from wab.utils.operator import OperatorMongo, MongoColumnType


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
                         ssl=False, user_id=0):
        str_cache_db = str(user_id) + host
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
                                     ssl=provider_connection.ssl,
                                     user_id=provider_connection.creator.id)

    def get_all_collections(self, db, cache_db=None):
        try:
            collections = db.list_collection_names()
            return collections
        except Exception as err:
            if cache_db:
                self.delete_cache_db_exception(cache_db)
            raise Exception(err)

    @staticmethod
    def get_all_documents(db, collection, column_sort, page=1, page_size=20, sort=pymongo.DESCENDING):
        if column_sort:
            documents = db[collection].find({}).sort(column_sort, sort).skip((page - 1) * page_size).limit(page_size)
        else:
            documents = db[collection].find({}).skip((page - 1) * page_size).limit(page_size)
        count = documents.count()
        return documents, count

    @staticmethod
    def get_all_keys(db, collection):
        try:
            cursor = db[collection].find({}).limit(1)
            for document in cursor:
                return document.keys()
        except Exception as err:
            raise Exception(err)

    @staticmethod
    def create_new_collection(db, collection_name):
        collection = db.create_collection(collection_name)
        return collection

    @staticmethod
    def create_new_field(db, collection_name, field_name, field_value):
        collection = db[collection_name]
        collection.insert({field_name: field_value})
        return collection

    @staticmethod
    def insert_data_collection(db, collection_name, list_data):
        collection = db[collection_name]
        collection.insert(list_data)

    @staticmethod
    def export_db_by_column(db, table, list_filter=None, list_column=None):
        collection = db[table]
        # if list_column:
        #     select_column = {}
        #     for c in list_column:
        #         select_column.update({c: 1})
        #     if list_filter:
        #         return collection.find(
        #             list_filter,
        #             select_column
        #         )
        #     else:
        #         return collection.find({}, select_column)
        # else:
        return collection.find({}).limit(1000)

    @staticmethod
    def check_column_data_type(db, table, column):
        result = db[table].aggregate(

            [
                {"$project": {"fieldType": {"$type": "$" + column}}},
                {"$limit": 1}
            ]
        )
        data = None
        for r in result:
            data = r['fieldType']
        return data
        # map = Code("function() { for (var key in this) { emit(key, [ typeof value[key] ]); } }")
        #
        # reduce = Code("function(key, stuff) { return (key, add_to_set(stuff) ); }")
        # result = db[table].map_reduce(map, reduce, "result")
        # return result

    def update_convert_column_data_type(self, db, table, column, data_type, provider_connection_id):
        real_data_type = self.check_column_data_type(db, table, column)
        if real_data_type == data_type:
            return True
        else:
            value, name = MongoColumnType.get_type(real_data_type)
            r_value, r_name = MongoColumnType.get_type(data_type)
            if r_name:
                operations = []
                collection = db[table]
                list_doc = collection.find({column: {"$exists": True, "$type": value}})
                if list_doc.count() > 1000:
                    CustomColumnTaskConvert.objects.create(
                        connection_id=provider_connection_id,
                        table_name=table,
                        column_name=column,
                        data_real_type=name,
                        data_type=data_type,
                        current_row=0
                    )
                else:
                    for doc in list_doc:
                        # Set a random number on every document update
                        operations.append(
                            UpdateOne({"_id": doc["_id"]},
                                      # {'$set': {column: {'$convert': {'input': doc.get(column), 'to': r_name}}}})
                                      {"$set": {column: self.convert_column_data_type(doc.get(column), r_name)}})
                        )

                        # Send once every 1000 in batch
                        collection.bulk_write(operations, ordered=False)
                        operations = []

                    if len(operations) > 0:
                        collection.bulk_write(operations, ordered=False)
            return True

    @staticmethod
    def convert_column_data_type(value, parse_to_type):
        if value:
            try:
                if parse_to_type == "string":
                    if type(value) is str:
                        return value
                    return str(value)
                elif parse_to_type == "bool":
                    if type(value) is bool:
                        return value
                    return bool(value)
                elif parse_to_type == "object":
                    if type(value) is dict:
                        return value
                    return None
                elif parse_to_type == "array":
                    if type(value) is list:
                        return [value]
                    return [value]
                elif parse_to_type == "int" or parse_to_type == "long":
                    if type(value) is int:
                        return value
                    return int(value)
                elif parse_to_type == "float" or parse_to_type == "decimal" or parse_to_type == "double":
                    if type(value) is float:
                        return value
                    return float(value)
                elif parse_to_type == "datetime":
                    date_time = datetime.strptime(value, "%d%m%Y_%H%M")
                    if type(date_time) is datetime:
                        return value
                    return None
            except Exception as err:
                print(str(err))
                return None
        else:
            return None

    @staticmethod
    def condition_filter(column, condition, value):
        item = {column: {"$eq": value}}
        if condition == OperatorMongo.get_value('operator_equals'):
            item = {column: {"$eq": value}}
        elif condition == OperatorMongo.get_value('operator_not_equals'):
            item = {column: {"$ne": value}}
        elif condition == OperatorMongo.get_value('operator_less_than'):
            item = {column: {"$lt": value}}
        elif condition == OperatorMongo.get_value('operator_less_than_or_equals'):
            item = {column: {"$lte": value}}
        elif condition == OperatorMongo.get_value('operator_greater_than'):
            item = {column: {"$gt": value}}
        elif condition == OperatorMongo.get_value('operator_greater_than_or_equals'):
            item = {column: {"$gte": value}}
        elif condition == OperatorMongo.get_value('operator_in'):
            item = {column: {"$in": [value]}}
        elif condition == OperatorMongo.get_value('operator_not_in'):
            item = {column: {"$nin": [value]}}
        elif condition == OperatorMongo.get_value('operator_contains'):
            value = f".*{value}.*"
            item = {column: {"$regex": value}}
        return item

    @staticmethod
    def condition_filter_operator(condition, value):
        operator = {"$eq": value}
        if condition == OperatorMongo.get_value('operator_equals'):
            operator = {"$eq": value}
        elif condition == OperatorMongo.get_value('operator_not_equals'):
            operator = {"$ne": value}
        elif condition == OperatorMongo.get_value('operator_less_than'):
            operator = {"$lt": value}
        elif condition == OperatorMongo.get_value('operator_less_than_or_equals'):
            operator = {"$lte": value}
        elif condition == OperatorMongo.get_value('operator_greater_than'):
            operator = {"$gt": value}
        elif condition == OperatorMongo.get_value('operator_greater_than_or_equals'):
            operator = {"$gte": value}
        elif condition == OperatorMongo.get_value('operator_in'):
            operator = {"$in": [value]}
        elif condition == OperatorMongo.get_value('operator_not_in'):
            operator = {"$nin": [value]}
        elif condition == OperatorMongo.get_value('operator_contains'):
            value = f".*{value}.*"
            operator = {"$regex": value}
        return operator

    def find_by_fk(self, db, table, custom_column_filter, page=1, page_size=20):
        # item = self.condition_filter(column, condition, value)
        # select_column = {column: 1}
        # documents = db[table].find(
        #     item,
        #     select_column
        # ).skip((page - 1) * page_size).limit(page_size)
        items = {}
        for i in custom_column_filter:
            items.update({i.field_name: self.condition_filter_operator(i.operator, i.value)})
        documents = db[table].find(
            items
        ).skip((page - 1) * page_size).limit(page_size)
        count = documents.count()
        return documents, count

    def union(self, db, table_1, field_1, table_2, field_2, condition_items, order_by, page=0, page_size=20):
        if order_by is None:
            order_by = field_1
        list_match_and_tb1 = []
        list_match_or_tb1 = []
        list_match_and_tb2 = []
        list_match_or_tb2 = []
        for condition in condition_items:
            if condition.table_name == table_1:
                item = self.condition_filter(condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and_tb1.append(item)
                else:
                    list_match_or_tb1.append(item)
            else:
                item = self.condition_filter("data." + condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and_tb2.append(item)
                else:
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

    # TODO: right join switch table
    def left_right_join(self, db, table_1, field_1, table_2, field_2, order_by, condition_items, page, page_size):
        if order_by is None:
            order_by = field_1
        collection = db[table_1]
        list_match_and = []
        list_match_or = []
        for condition in condition_items:
            if condition.table_name == table_1:
                item = self.condition_filter(condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and.append(item)
                else:
                    list_match_or.append(item)
            else:
                item = self.condition_filter("data." + condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and.append(item)
                else:
                    list_match_or.append(item)
        pipeline = []
        if len(list_match_and) > 0 and len(list_match_or) > 0:
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
                # {"$unwind": "$data"},
                {
                    "$match": {
                        "$and": list_match_and,
                        "$or": list_match_or
                    }
                },
                {"$sort": {order_by: -1}},
                # {
                #     "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
                # },
                {
                    "$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$data", 0]}, "$$ROOT"]}}
                },
                {
                    "$project": {"data": 0, "_id": 0}
                }
            ]
        else:
            if len(list_match_and) > 0:
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
                    # {"$unwind": "$data"},
                    {
                        "$match": {
                            "$and": list_match_and
                        }
                    },
                    {"$sort": {order_by: -1}},
                    # {
                    #     "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
                    # },
                    {
                        "$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$data", 0]}, "$$ROOT"]}}
                    },
                    {
                        "$project": {"data": 0, "_id": 0}
                    }
                ]
            elif len(list_match_or) > 0:
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
                    # {"$unwind": "$data"},
                    {
                        "$match": {
                            "$or": list_match_or
                        }
                    },
                    {"$sort": {order_by: -1}},
                    # {
                    #     "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
                    # },
                    {
                        "$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$data", 0]}, "$$ROOT"]}}
                    },
                    {
                        "$project": {"data": 0, "_id": 0}
                    }
                ]
            else:
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
                    # {"$unwind": "$data"},
                    {"$sort": {order_by: -1}},
                    # {
                    #     "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
                    # },
                    {
                        "$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$data", 0]}, "$$ROOT"]}}
                    },
                    {
                        "$project": {"data": 0, "_id": 0}
                    }
                ]
        return collection.aggregate(pipeline)

    def inner_join(self, db, table_1, field_1, table_2, field_2, order_by, condition_items, page, page_size):
        if order_by is None:
            order_by = field_1
        collection = db[table_1]
        list_match_and = []
        list_match_or = []
        for condition in condition_items:
            if condition.table_name == table_1:
                item = self.condition_filter(condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and.append(item)
                else:
                    list_match_or.append(item)
            else:
                item = self.condition_filter("data." + condition.field_name, condition.operator, condition.value)
                if condition.relation is None or condition.relation == Relation.get_value('relation_and'):
                    list_match_and.append(item)
                else:
                    list_match_or.append(item)
        if len(list_match_and) > 0 and len(list_match_or) > 0:
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
        else:
            if len(list_match_and) > 0:
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
                            "$and": list_match_and
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
            elif len(list_match_or) > 0:
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
            else:
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
                    {"$sort": {order_by: -1}},
                    {
                        "$replaceRoot": {"newRoot": {"$mergeObjects": ["$data", "$$ROOT"]}}
                    },
                    {
                        "$project": {"data": 0, "_id": 0}
                    }
                ]

        return collection.aggregate(pipeline)

    def right_outer_join(self, db, table_1, field_1, table_2, field_2, order_by, condition_items, page, page_size):
        pass

    def sql_function_exe(self, sql_function=None, db=None, page=1, page_size=20):
        sql_function_merge = SqlFunctionMerge.objects.filter(sql_function=sql_function)
        order_bys = SqlFunctionOrderBy.objects.filter(sql_function=sql_function)
        order_by = None
        if order_bys.exists():
            order_by = order_bys.first().order_by_name
        condition_items = SqlFunctionConditionItems.objects.filter(sql_function=sql_function)
        if len(sql_function_merge) >= 2:
            merge_type = MergeType.left_join
            table_name_first = None
            column_name_first = None
            table_name_second = None
            column_name_second = None
            for index, merge in enumerate(sql_function_merge):
                table_name_first = merge.table_name
                column_name_first = merge.column_name
                merge_type = merge.merge_type
                merge_after = sql_function_merge[index + 1]
                table_name_second = merge_after.table_name
                column_name_second = merge_after.column_name
                break
            if merge_type == MergeType.left_join.get_name(member='left_join'):
                return self.left_right_join(db=db, table_1=table_name_first, field_1=column_name_first,
                                            table_2=table_name_second, field_2=column_name_second,
                                            order_by=order_by, condition_items=condition_items,
                                            page=page, page_size=page_size)
            elif merge_type == MergeType.right_join.get_name(member='right_join'):
                return self.left_right_join(db=db, table_1=table_name_second, field_1=column_name_second,
                                            table_2=table_name_first, field_2=column_name_first,
                                            order_by=order_by, condition_items=condition_items,
                                            page=page, page_size=page_size)
            elif merge_type == MergeType.inner_join.get_name(member='inner_join'):
                return self.inner_join(db=db, table_1=table_name_first, field_1=column_name_first,
                                       table_2=table_name_second, field_2=column_name_second,
                                       order_by=order_by, condition_items=condition_items,
                                       page=page, page_size=page_size)
            elif merge_type == MergeType.union.get_name(member='union'):
                return self.union(db=db, table_1=table_name_first, field_1=column_name_first,
                                  table_2=table_name_second, field_2=column_name_second,
                                  order_by=order_by, condition_items=condition_items,
                                  page=page, page_size=page_size)
            elif merge_type == MergeType.right_outer_join.get_name(member='right_outer_join'):
                return self.right_outer_join(db=db, table_1=table_name_first, field_1=column_name_first,
                                             table_2=table_name_second, field_2=column_name_second,
                                             order_by=order_by, condition_items=condition_items,
                                             page=page, page_size=page_size)
            else:
                return None
        else:
            return None

    def create_table_with_sql_function(self, db, collection, sql_function):
        pass


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
