# Generated by Django 5.2.1 on 2025-07-09 00:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0005_driver_constructor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fantasyteam',
            name='race',
        ),
        migrations.AlterField(
            model_name='fantasyteam',
            name='driver_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fantasy_teams_1', to='fantasy.driver'),
        ),
        migrations.AlterField(
            model_name='fantasyteam',
            name='driver_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fantasy_teams_2', to='fantasy.driver'),
        ),
        migrations.AlterField(
            model_name='fantasyteam',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
