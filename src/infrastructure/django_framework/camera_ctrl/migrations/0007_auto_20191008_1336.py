# Generated by Django 2.2.4 on 2019-10-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera_ctrl', '0006_generalsettings_nb_of_failures_to_reboot_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalsettings',
            name='email_subject_prefix',
            field=models.CharField(blank=True, default='[nucpcaps5]', max_length=64),
        ),
    ]
