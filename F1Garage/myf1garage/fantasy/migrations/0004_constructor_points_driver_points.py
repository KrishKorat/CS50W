# Generated by Django 5.2.1 on 2025-07-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0003_remove_fantasyteam_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructor',
            name='points',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='driver',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
