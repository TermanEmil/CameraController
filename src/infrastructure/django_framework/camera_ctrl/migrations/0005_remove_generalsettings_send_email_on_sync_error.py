# Generated by Django 2.2.4 on 2019-10-06 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camera_ctrl', '0004_generalsettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalsettings',
            name='send_email_on_sync_error',
        ),
    ]
