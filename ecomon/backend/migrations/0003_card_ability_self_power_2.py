# Generated by Django 5.1.6 on 2025-02-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0002_delete_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="ability_self_power_2",
            field=models.IntegerField(default=0),
        ),
    ]
