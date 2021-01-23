from config.celery_app import app


@app.task
def process_export_database():
    from wab.core.export_database.models import ExportData
    from wab.utils.constant import MONGO
    from wab.utils.db_manager import MongoDBManager
    import json
    from bson.json_util import dumps
    from django.conf import settings
    from datetime import datetime
    import io
    import xlsxwriter
    from wab.core.notifications.models import PUSH_NOTIFICATION, NOTIFY
    from wab.core.notifications.services.notifications_service import NotificationsService

    export_data = ExportData.objects.filter(status=ExportData.INIT)
    today = datetime.now().strftime("%d%m%Y_%H%M%S")
    for e in export_data:
        e.status = ExportData.RUNNING
        e.save()
    export_data = ExportData.objects.filter(status=ExportData.RUNNING)
    for export in export_data:
        if export.provider_connection.provider.name == MONGO:
            mongo_db_manager = MongoDBManager()
            db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=export.provider_connection)
            documents = mongo_db_manager.export_db_by_column(db=db, table=export.table,
                                                             list_filter=export.list_filter,
                                                             list_column=export.list_column)
            result = json.loads(dumps(list(documents)))
            headers = list(result[0].keys())
            if export.file_type == ExportData.TXT:
                content = ''
                for header in headers:
                    content += header
                    if headers.index(header) != len(headers) - 1:
                        content += ', '
                    else:
                        content += '\n'

                for value in result:
                    for header in headers:
                        if header == "_id":
                            content += value.get(header).get('$oid')
                        else:
                            try:
                                content += value.get(header)
                            except:
                                content += ''
                        if headers.index(header) != len(headers) - 1:
                            content += ', '
                        else:
                            content += '\n'

                filename = f"ExportData-{export.table}-{today}.txt"
                file_path = f"{settings.MEDIA_ROOT}\export\\{filename}"

                with io.open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                export.file_path = file_path
                export.save()

                payload_single = {
                    "channel": PUSH_NOTIFICATION,
                    "title": "Export data success",
                    "body": f"System export data success for {export.username}",
                    "username": export.username,
                    "data": {
                        "username": export.username,
                        "action": "export_data",
                        "url": f"/core/download/{export.table}/{str(export.id)}/",
                        "export_id": export.id,
                        "notification_type": NOTIFY
                    }
                }
                notify_service = NotificationsService()
                notify_service.process_push_single_notification(data=payload_single)

            elif export.file_type == ExportData.EXCEL:
                filename = f"ExportData-{export.table}-{today}.xlsx"
                file_path = f"{settings.MEDIA_ROOT}\export\\{filename}"
                workbook = xlsxwriter.Workbook(file_path)
                worksheet = workbook.add_worksheet()

                cell_format_header = workbook.add_format()
                cell_format_header.set_bold()

                for index in range(len(headers)):
                    worksheet.write(0, index, headers[index], cell_format_header)

                for row_num, columns in enumerate(result):
                    for index in range(len(headers)):
                        value = columns.get(headers[index]) if index != 0 else columns.get(headers[index]).get('$oid')
                        worksheet.write(row_num + 1, index, value)

                workbook.close()

                export.file_path = file_path
                export.save()
                payload_single = {
                    "channel": PUSH_NOTIFICATION,
                    "title": "Export data success",
                    "body": f"System export data success for {export.username}",
                    "username": export.username,
                    "data": {
                        "username": export.username,
                        "action": "export_data",
                        "url": f"/core/download/{export.table}/{str(export.id)}/",
                        "export_id": export.id,
                        "notification_type": NOTIFY
                    }
                }
                notify_service = NotificationsService()
                notify_service.process_push_single_notification(data=payload_single)

            elif export.file_type == ExportData.PDF:
                # TODO: Sae File PDF
                pass

            export.status = ExportData.COMPLETE
            export.save()
