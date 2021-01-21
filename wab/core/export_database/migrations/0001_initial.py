# Generated by Django 3.0.11 on 2021-01-21 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('db_provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
                ('table', models.CharField(blank=True, max_length=128, null=True)),
                ('file_path', models.CharField(blank=True, max_length=128, null=True)),
                ('status', models.CharField(choices=[('init', 'init'), ('running', 'running'), ('complete', 'complete')], default='init', max_length=20)),
                ('file_type', models.CharField(choices=[('excel', 'excel'), ('txt', 'txt'), ('pdf', 'pdf')], default='txt', max_length=20)),
                ('provider_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_provider.DBProviderConnection')),
            ],
            options={
                'db_table': 'export_data',
            },
        ),
    ]
