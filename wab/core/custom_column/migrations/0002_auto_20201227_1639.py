# Generated by Django 3.0.11 on 2020-12-27 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom_column', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomColumnConfigType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigtype_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigtype_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'db_table': 'custom_column_config_type',
            },
        ),
        migrations.CreateModel(
            name='CustomColumnConfigTypeValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigtypevalidator_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('custom_column_config_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_column.CustomColumnConfigType')),
            ],
            options={
                'db_table': 'custom_column_config_type_validator',
            },
        ),
        migrations.CreateModel(
            name='CustomColumnConfigValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_protect', models.BooleanField(default=False)),
                ('function', models.CharField(blank=True, max_length=255, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigvalidation_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'db_table': 'custom_column_config_validation',
            },
        ),
        migrations.CreateModel(
            name='CustomColumnRegexType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('time_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Last modified on')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnregextype_creator', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnregextype_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'db_table': 'custom_column_regex_type',
            },
        ),
        migrations.RemoveField(
            model_name='validationregex',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='validationregex',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='validationtype',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='validationtype',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='customcolumntype',
            name='type',
        ),
        migrations.DeleteModel(
            name='ColumnValidation',
        ),
        migrations.DeleteModel(
            name='ValidationRegex',
        ),
        migrations.DeleteModel(
            name='ValidationType',
        ),
        migrations.AddField(
            model_name='customcolumnconfigvalidation',
            name='custom_column_regex_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_column.CustomColumnRegexType'),
        ),
        migrations.AddField(
            model_name='customcolumnconfigvalidation',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigvalidation_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by'),
        ),
        migrations.AddField(
            model_name='customcolumnconfigtypevalidator',
            name='custom_column_config_validation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_column.CustomColumnConfigValidation'),
        ),
        migrations.AddField(
            model_name='customcolumnconfigtypevalidator',
            name='custom_column_regex_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_column.CustomColumnRegexType'),
        ),
        migrations.AddField(
            model_name='customcolumnconfigtypevalidator',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_column_customcolumnconfigtypevalidator_last_modified', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by'),
        ),
        migrations.AddField(
            model_name='customcolumntype',
            name='custom_column_config_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_column.CustomColumnConfigType'),
        ),
    ]
