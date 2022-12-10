# Generated by Django 4.1.3 on 2022-12-10 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_end_alter_event_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateProposalVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.dateproposal')),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.usertoevent')),
            ],
            options={
                'unique_together': {('proposal', 'voting')},
            },
        ),
    ]