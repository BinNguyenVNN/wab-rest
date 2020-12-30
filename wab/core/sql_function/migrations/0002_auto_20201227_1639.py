# Generated by Django 3.0.11 on 2020-12-27 09:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sql_function', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sqlfunctionconditionitems',
            name='table_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sqlfunctionconditionitems',
            name='operator',
            field=models.CharField(blank=True, choices=[('=', '='), ('in', 'in'), ('contain', 'contain')], default='=',
                                   max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='sqlfunctionconditionitems',
            name='relation',
            field=models.CharField(blank=True, choices=[('and', 'and'), ('or', 'or')], default=None, max_length=32,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='sqlfunctionmerge',
            name='merge_type',
            field=models.CharField(blank=True, choices=[('inner join', 'inner join'), ('left join', 'left join'),
                                                        ('right join', 'right join'),
                                                        ('right outer join', 'right outer join'), ('union', 'union')],
                                   default='inner join', max_length=32, null=True),
        ),
    ]
