# Generated by Django 2.2.3 on 2019-08-15 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0007_auto_20190815_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelapse',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduling.CronSchedule'),
        ),
    ]
