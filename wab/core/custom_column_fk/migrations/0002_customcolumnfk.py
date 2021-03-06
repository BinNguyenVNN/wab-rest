# Generated by Django 3.0.11 on 2020-12-27 09:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db_provider', '0001_initial'),
        ('custom_column_fk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomColumnFK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('table_name', models.CharField(blank=True, max_length=255, null=True)),
                ('field_name', models.CharField(blank=True, max_length=255, null=True)),
                ('operator',
                 models.CharField(blank=True, choices=[('in', 'in'), ('contain', 'contain')], default='contain',
                                  max_length=32, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('connection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                 to='db_provider.DBProviderConnection')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='custom_column_fk_customcolumnfk_creator',
                                              to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='custom_column_fk_customcolumnfk_last_modified',
                                   to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'db_table': 'custom_column_fk',
            },
        ),
    ]
