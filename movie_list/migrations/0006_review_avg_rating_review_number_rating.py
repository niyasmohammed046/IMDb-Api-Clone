# Generated by Django 5.0.1 on 2024-01-31 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_list', '0005_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
    ]
