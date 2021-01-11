# Generated by Django 3.0.11 on 2021-01-11 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db_provider', '0001_initial'),
        ('custom_column', '0006_auto_20210109_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomColumnTaskConvert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(blank=True, max_length=255, null=True)),
                ('column_name', models.CharField(blank=True, max_length=255, null=True)),
                ('data_real_type', models.CharField(blank=True, max_length=255, null=True)),
                ('data_type', models.CharField(blank=True, max_length=255, null=True)),
                ('current_row', models.IntegerField(default=0)),
                ('connection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_provider.DBProviderConnection')),
            ],
        ),
    ]
