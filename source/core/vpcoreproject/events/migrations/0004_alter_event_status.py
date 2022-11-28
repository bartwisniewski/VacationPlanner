# Generated by Django 4.1.3 on 2022-11-28 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_dateproposal_event_remove_dateproposal_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.IntegerField(choices=[(0, 'Date selection'), (1, 'Place selection'), (2, 'Booking'), (3, 'Confirmed'), (4, 'Historical')], default=0),
        ),
    ]
