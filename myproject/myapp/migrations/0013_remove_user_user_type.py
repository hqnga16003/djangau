# Generated by Django 4.2.11 on 2024-04-23 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_location_name_alter_user_email_busroute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]
