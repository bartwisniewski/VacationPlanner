# Generated by Django 4.1.3 on 2022-12-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_alter_event_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="end",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="start",
            field=models.DateField(null=True),
        ),
    ]
