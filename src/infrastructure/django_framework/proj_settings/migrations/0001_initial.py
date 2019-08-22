# Generated by Django 2.2.4 on 2019-08-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_email_on_error', models.BooleanField(default=True)),
                ('log_to_db_timelapse_capture', models.BooleanField(default=False, verbose_name='Log timelapse capture')),
                ('log_to_db_camera_capture', models.BooleanField(default=False, verbose_name='Log camera capture')),
                ('autodetect_cameras_on_start', models.BooleanField(default=True)),
                ('emails', models.CharField(blank=True, help_text='Space separated emails', max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]