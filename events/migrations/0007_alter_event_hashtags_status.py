# Generated by Django 4.2.2 on 2023-07-05 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_hashtags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_hashtags',
            name='status',
            field=models.CharField(max_length=255),
        ),
    ]