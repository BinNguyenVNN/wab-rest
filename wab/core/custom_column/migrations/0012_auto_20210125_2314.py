# Generated by Django 3.0.11 on 2021-01-25 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_column', '0011_auto_20210115_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcolumnconfigvalidation',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='customcolumnmapping',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='customcolumntype',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='customcolumntypevalidator',
            options={'ordering': ['-id']},
        ),
    ]
