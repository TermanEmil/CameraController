# Generated by Django 2.2.4 on 2019-09-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj_settings', '0008_auto_20190830_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalsettings',
            name='email_subject_prefix',
            field=models.CharField(blank=True, default='[Emils-MacBook-Pro.local]', max_length=64),
        ),
    ]
