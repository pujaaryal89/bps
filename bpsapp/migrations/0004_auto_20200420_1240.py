# Generated by Django 3.0.5 on 2020-04-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpsapp', '0003_auto_20200420_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='interests',
            field=models.ManyToManyField(to='bpsapp.LocationCategory'),
        ),
    ]
