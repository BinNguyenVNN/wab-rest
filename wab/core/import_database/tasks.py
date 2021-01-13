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
    import csv
    import os

    default_length = 20
    import_data = ImportData.objects.all()
    for data in import_data:
        if data.provider_connection.provider.name == MONGO:
            table_name = data.table
            connection = DBProviderConnection.objects.filter(id=data.provider_connection.id).first()
            mongo_db_manager = MongoDBManager()
            db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
            # collections = mongo_db_manager.get_all_collections(db=db, cache_db=cache_db)
            # if table_name not in collections:
            #     # table_name ko tồn tại, pass
            #     continue
            table = db[table_name]

            max_records = []
            with open(data.file_url, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    max_records.append(row)

            records = max_records[:default_length]

            for i in range(len(records)):
                row = records[i]
                records[i]["_id"] = ObjectId(row.get("_id")) if row.get("_id") else ObjectId()

            insert = table.insert_many(records)
            response_id = []
            for ids in insert.inserted_ids:
                response_id.append(str(ids))
            print(response_id)

            new_record = max_records[default_length:]

            if len(new_record) > 0:
                file = open(data.file_url, 'w')
                with file:
                    header = new_record[0].keys()
                    writer = csv.DictWriter(file, fieldnames=header)
                    writer.writeheader()
                    for r in new_record:
                        writer.writerow(r)

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

                os.remove(data.file_url)
                data.delete()
