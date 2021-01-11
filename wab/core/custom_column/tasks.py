from config.celery_app import app


@app.task
def process_convert_data():
    from wab.core.custom_column.models import CustomColumnTaskConvert
    from wab.core.db_provider.models import DBProviderConnection
    from wab.utils.db_manager import MongoDBManager
    from wab.utils.operator import MongoColumnType
    from pymongo import UpdateOne
    from wab.core.notifications.models import PUSH_NOTIFICATION
    from wab.core.notifications.services.notifications_service import NotificationsService
    from wab.core.notifications.models import NOTIFY

    convert_data = CustomColumnTaskConvert.objects.all()
    for data in convert_data:
        mongo_db = MongoDBManager()
        provider_connection = DBProviderConnection.objects.filter(id=data.connection.id).first()
        db, cache_db = mongo_db.connection_mongo_by_provider(provider_connection=provider_connection)

        value, name = MongoColumnType.get_type(data.data_real_type)
        r_value, r_name = MongoColumnType.get_type(data.data_type)
        if r_name:
            operations = []
            collection = db[data.table_name]
            list_doc = collection.find({data.column_name: {"$exists": True, "$type": value}}).limit(1000)
            for doc in list_doc:
                # Set a random number on every document update
                operations.append(
                    UpdateOne({"_id": doc["_id"]},
                              {"$set": {
                                  data.column_name: mongo_db.convert_column_data_type(doc.get(data.column_name),
                                                                                      r_name)}})
                )

                # Send once every 1000 in batch
                collection.bulk_write(operations, ordered=False)
                operations = []
            if len(operations) > 0:
                collection.bulk_write(operations, ordered=False)

            # Note: list_doc.count() will count all select, not include skip & limit
            if list_doc.count() != 0:
                data.current_row += 1000
                data.save()
            else:
                data.delete()
                payload_single = {
                    "channel": PUSH_NOTIFICATION,
                    "title": "Convert data success",
                    "body": f"Send to {data.connection.creator.username}, system convert data success!",
                    "username": data.connection.creator.username,
                    "data": {
                        "username": data.connection.creator.username,
                        "notification_type": NOTIFY
                    }
                }
                notify_service = NotificationsService()
                notify_service.process_push_single_notification(data=payload_single)
