# Generated by Django 3.0.11 on 2021-01-15 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_column', '0009_auto_20210115_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcolumntypevalidator',
            name='operator',
            field=models.CharField(blank=True, choices=[('in', 'in'), ('not_in', 'not in'), ('contains', 'regex'), ('equals', '='), ('not_equals', '!='), ('less_than', '<'), ('less_than_or_equals', '<='), ('greater_than', '>'), ('less_greater_than_or_equals', '>=')], default='equals', max_length=32, null=True),
        ),
    ]
