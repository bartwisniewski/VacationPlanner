# Generated by Django 4.1.3 on 2022-11-28 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dateproposal',
            name='event',
        ),
        migrations.RemoveField(
            model_name='dateproposal',
            name='user',
        ),
        migrations.RemoveField(
            model_name='placeproposal',
            name='event',
        ),
        migrations.RemoveField(
            model_name='placeproposal',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserToEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('owner', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dateproposal',
            name='user_event',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='events.usertoevent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='placeproposal',
            name='user_event',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='events.usertoevent'),
            preserve_default=False,
        ),
    ]
