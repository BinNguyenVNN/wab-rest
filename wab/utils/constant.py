from django.utils.translation import ugettext_lazy as _

MONGO, POSTGRES, MYSQL = ('MongoDB', 'Postgres', 'MySQL')

DATABASE_LIST = (
    (MONGO, _("Mongo Database")),
    (POSTGRES, _("Postgres Database")),
    (MYSQL, _("MySQL Database")),
)

MONGO_SRV_CONNECTION, MONGO_CONNECTION = ('mongodb+srv', 'mongodb')
