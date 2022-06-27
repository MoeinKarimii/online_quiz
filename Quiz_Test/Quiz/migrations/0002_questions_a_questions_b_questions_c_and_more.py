# Generated by Django 4.0.4 on 2022-05-07 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='a',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='b',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='c',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='correct_answer',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='questions',
            name='d',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
    ]