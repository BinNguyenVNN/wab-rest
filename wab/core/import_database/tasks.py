from config.celery_app import app


@app.task
def process_import_database():
    from wab.core.notifications.services.notifications_service import NotificationsService
    from wab.core.import_database.models import ImportData
    from wab.utils.constant import MONGO
    from wab.core.db_provider.models import DBProviderConnection
    from wab.utils.db_manager import MongoDBManager
    from wab.core.notifications.models import PUSH_NOTIFICATION, NOTIFY
    from bson import ObjectId

    default_length = 20
    import_data = ImportData.objects.all()
    for data in import_data:
        if data.provider_connection.provider.name == MONGO:
            table_name = data.table
            connection = DBProviderConnection.objects.filter(id=data.provider_connection.id).first()
            mongo_db_manager = MongoDBManager()
            db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
            collections = mongo_db_manager.get_all_collections(db=db)
            if table_name not in collections:
                # table_name ko tồn tại, pass
                continue
            table = db[table_name]

            if len(data.record) > default_length:
                records = data.record[:default_length]
            else:
                records = data.record

            for i in range(len(records)):
                row = records[i]
                records[i]["_id"] = ObjectId(row.get("_id")) if row.get("_id") else ObjectId()

            insert = table.insert_many(records)
            response_id = []
            for ids in insert.inserted_ids:
                response_id.append(str(ids))
            print(response_id)

            new_record = data.record[default_length:]
            data.record = new_record
            if len(data.record) > 0:
                data.save()
            else:
                payload_single = {
                    "channel": PUSH_NOTIFICATION,
                    "title": "Insert data success",
                    "body": f"{data.username} insert data success",
                    "username": data.username,
                    "data": {
                        "username": data.username,
                        "notification_type": NOTIFY
                    }
                }
                notify_service = NotificationsService()
                notify_service.process_push_single_notification(data=payload_single)
                data.delete()
