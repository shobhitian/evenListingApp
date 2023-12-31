# Generated by Django 4.2.2 on 2023-07-05 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_hashtags',
            name='status',
            field=models.CharField(choices=[('1', 'active'), ('2', 'inactive')], max_length=255),
        ),
        migrations.AlterField(
            model_name='hashtags',
            name='status',
            field=models.CharField(choices=[('1', 'pending'), ('2', 'approved'), ('3', 'suspended')], max_length=255),
        ),
    ]
