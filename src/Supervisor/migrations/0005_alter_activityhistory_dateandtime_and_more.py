# Generated by Django 4.2.19 on 2025-02-21 08:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Supervisor', '0004_activityhistory_connectionrequesthistory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityhistory',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 21, 16, 44, 15, 71689)),
        ),
        migrations.AlterField(
            model_name='pendingconnections',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 21, 16, 44, 15, 71223)),
        ),
    ]
