# Generated by Django 4.0.4 on 2022-05-09 11:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0007_alter_questionitems_question_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionitems',
            name='user_answer',
            field=models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='thequiz',
            name='created_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 5, 9, 11, 28, 38, 387054, tzinfo=utc)),
        ),
    ]
