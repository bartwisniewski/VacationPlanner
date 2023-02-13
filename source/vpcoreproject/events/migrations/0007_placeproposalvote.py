# Generated by Django 4.1.3 on 2022-12-12 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_dateproposalvote"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaceProposalVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.placeproposal",
                    ),
                ),
                (
                    "voting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.usertoevent",
                    ),
                ),
            ],
            options={
                "unique_together": {("proposal", "voting")},
            },
        ),
    ]
