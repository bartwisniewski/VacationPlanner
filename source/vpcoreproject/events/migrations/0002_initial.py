# Generated by Django 4.1.3 on 2022-11-28 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("places", "0001_initial"),
        ("friends", "0001_initial"),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="placeproposal",
            name="place",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="places.place"
            ),
        ),
        migrations.AddField(
            model_name="placeproposal",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="friends.usertofriends"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="friends",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="friends.friends"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="place",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="places.place",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="promoter",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="friends.usertofriends",
            ),
        ),
        migrations.AddField(
            model_name="dateproposal",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="events.event"
            ),
        ),
        migrations.AddField(
            model_name="dateproposal",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="friends.usertofriends"
            ),
        ),
    ]
