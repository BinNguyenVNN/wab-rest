# Generated by Django 3.0.11 on 2021-01-23 13:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exportdata',
            name='list_column',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
        migrations.AddField(
            model_name='exportdata',
            name='list_filter',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
    ]
