import json

from bson.json_util import dumps
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.utils import responses, constant
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class SqlViewTest(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()

    def get(self, request):
        provider_connection = self.queryset.get(id=1)
        provider = provider_connection.provider
        if provider:
            if provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                collection = db["order_items"]
                pipeline = [
                    {
                        "$match": {"product_id": "ef92defde845ab8450f9d70c526ef70f"}
                    },
                    {"$limit": 1},
                    { "$project": { "_id": '$$REMOVE' } },
                    {"$lookup": {
                        "from": 'order_reviews', "pipeline": [
                            {"$limit": 1},
                            {
                                "$match": {"review_score": "5"}
                            },
                        ], "as": 'order_reviews'}},
                    {"$lookup": {
                        "from": 'order_items', "pipeline": [
                            {
                                "$match": {"product_id": "ef92defde845ab8450f9d70c526ef70f"}
                            },
                        ], "as": 'order_items'}},
                    {
                        "$project":
                            {
                                "Union": {"$setUnion": ["$order_items", "$order_reviews"]}
                            }
                    },
                    {"$unwind": "$Union"},
                    {"$replaceRoot": {"newRoot": "$Union"}}
                    # {
                    #     "$match": {"product_id": "ef92defde845ab8450f9d70c526ef70f"}
                    # },
                    # {
                    #
                    #     "$lookup": {
                    #         "from": "order_reviews",
                    #         "pipeline": [
                    #             {"$limit": 20},
                    #             {"$project": {"_id": 0, "review_score": 1}},
                    #             {
                    #                 "$match": {"review_score": "5"}
                    #             },
                    #         ],
                    #         "as": "order_reviews"
                    #     }
                    # },
                    # {"$unwind": "$order_reviews"},
                    # {
                    #     "$group": {
                    #         "_id": "$_id",
                    #         "order_items": {
                    #             "$push": {
                    #                 "type": "order_items",
                    #                 "price": "$price",
                    #             }
                    #         },
                    #         "order_reviews": {
                    #             "$first": "$order_reviews"
                    #         },
                    #     }
                    # },
                    # {
                    #     "$project": {
                    #         "items": {
                    #             "$setUnion": ["$order_items", "$order_reviews"]
                    #         }
                    #     }
                    # },
                    # {
                    #     "$unwind": "$items"
                    # },
                    # {
                    #     "$replaceRoot": {
                    #         "newRoot": "$items"
                    #     }
                    # }
                    # },
                    # {
                    #     "$project": {
                    #         "_id": 1,
                    #         "price": 1,
                    #         "review_score": 1,
                    #     }
                    # }
                ]
                pipeline1 = [
                    {"$limit": 20},
                    {
                        "$lookup": {
                            "from": "order_reviews",
                            "pipeline": [
                                {"$limit": 20},
                                {"$project": {"_id": 0, "review_score": 1}},
                                {
                                    "$match": {"review_score": "5"}
                                },
                            ],
                            "as": "order_reviews"
                        }
                    },
                    {"$addFields":
                        {
                            "order_reviews": {
                                "$map": {
                                    "input": "$order_reviews",
                                    "as": "tbl2",
                                    "in": {
                                        "_id": "$$tbl2._id",
                                        "type": "order_reviews",
                                        "review_score": "$$tbl2.review_score",
                                    }
                                }
                            }
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "order_items": {
                                "$push": {
                                    "_id": "$_id",
                                    "type": "order_items",
                                    "price": "$price",
                                }
                            },
                            "order_reviews": {
                                "$first": "$order_reviews"
                            }
                        }
                    },
                    {
                        "$project": {
                            "items": {
                                "$setUnion": ["$order_items", "$order_reviews"]
                            }
                        }
                    },
                    {
                        "$unwind": "$items"
                    },
                    {
                        "$replaceRoot": {
                            "newRoot": "$items"
                        }
                    }
                ]
                # pipeline = [
                #     {
                #         "$match":
                #             {
                #                 "order_id": "00048cc3ae777c65dbb7d2a0634bc1ea"
                #             }
                #     },
                #     {"$project": {"_id": '$$REMOVE'}},
                #     {"$lookup": {"from": 'order_reviews', "pipeline": [
                #         {
                #             "$match":
                #                 {
                #                     "order_id": "00048cc3ae777c65dbb7d2a0634bc1ea"
                #                 }
                #         }
                #     ], "as": 'order_reviews'}},
                #     {"$lookup": {"from": 'order_items', "pipeline": [
                #         {
                #             "$match":
                #                 {
                #                     "order_id": "00048cc3ae777c65dbb7d2a0634bc1ea"
                #                 }
                #         }
                #     ], "as": 'order_items'}},
                #     # {
                #     #     "$project":
                #     #         {
                #     #             "Union": {"$concatArrays": ["$order_reviews", "$order_items"]}
                #     #         }
                #     # },
                #     #
                #     # {"$unwind": "$Union"},
                #     # {"$replaceRoot": {"newRoot": "$Union"}}
                #     { "$unwind": {"path": "$order_reviews", "preserveNullAndEmptyArrays": True}},
                #     { "$unwind": {"path": "$order_items", "preserveNullAndEmptyArrays": True}}
                # ]
                # pipeline = [
                #     {
                #         "$lookup": {
                #             "from": "order_reviews",
                #             "localField": "order_id",
                #             "foreignField": "order_id",
                #             "as": "data"
                #         }
                #     },
                #     {"$unwind": "$data"},
                #     {"$match": {
                #         "$and": [
                #             {"order_id": "a548910a1c6147796b98fdf73dbeba33"},
                #             {"data.review_id": "80e641a11e56f04c1ad469d5645fdfde"}
                #         ]}},
                #     {"$sort": {"order_id": -1}}
                #
                # ]
                c = collection.aggregate(pipeline)
                data = list(c)
                result = json.loads(dumps(data))
                return responses.ok(data=result, method=constant.GET, entity_name='sql_function')
