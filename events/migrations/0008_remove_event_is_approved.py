# Generated by Django 4.2.2 on 2023-07-05 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_event_hashtags_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_approved',
        ),
    ]
