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
                    {"$limit": 5},
                    {"$facet": {
                        "collection1": [
                            {"$limit": 10},
                            {"$lookup": {
                                "from": "order_items",
                                "pipeline": [
                                    {"$match": {
                                        # "date": {"$gte": ISODate("2018-09-01"), "$lte": ISODate("2018-09-10")},
                                        #"order_id": "a548910a1c6147796b98fdf73dbeba33"
                                        "price": {"$gte": 100}
                                    }},
                                    # {"$project": {
                                    #     "_id": 0, "price": 1
                                    # }}
                                ],
                                "as": "collection1"
                            }}
                        ],
                        "collection2": [
                            {"$limit": 10},
                            {"$lookup": {
                                "from": "order_reviews",
                                "pipeline": [
                                    {"$match": {
                                        # "order_id": "a548910a1c6147796b98fdf73dbeba33",
                                        "review_score": "1"
                                    }},
                                    # {"$project": {
                                    #     "_id": 0, "review_score": 1
                                    # }}
                                ],
                                "as": "collection2"
                            }}
                        ]
                    }},
                    {"$project": {
                        "data": {
                            "$concatArrays": [
                                {"$arrayElemAt": ["$collection1.collection1", 0]},
                                {"$arrayElemAt": ["$collection2.collection2", 0]},
                            ]
                        }
                    }},
                    {"$project": {
                        "item": {
                            "$mergeObjects": "$data"
                        }
                    }},
                    {"$unwind": "$item"},
                    {"$replaceRoot": {"newRoot": "$item"}},
                    # {"$sort": {"dated": -1}}
                ]
                c = collection.aggregate(pipeline)
                data = list(c)
                result = json.loads(dumps(data))
                return responses.ok(data=result, method=constant.GET, entity_name='sql_function')
