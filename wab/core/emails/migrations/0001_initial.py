# Generated by Django 3.0.9 on 2020-09-10 04:16

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('code', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True,
                                          verbose_name='Specific code for core app')),
                ('is_protected', models.BooleanField(default=False, verbose_name='Is protected')),
                ('content', models.TextField(verbose_name='Html content')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='emails_emailtemplate_creator', to=settings.AUTH_USER_MODEL,
                                              verbose_name='Created by')),
                ('last_modified_by',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                   related_name='emails_emailtemplate_last_modified', to=settings.AUTH_USER_MODEL,
                                   verbose_name='Last modified by')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
