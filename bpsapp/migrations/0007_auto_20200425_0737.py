# Generated by Django 3.0.5 on 2020-04-25 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bpsapp', '0006_auto_20200424_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationreview',
            name='reply',
        ),
        migrations.AddField(
            model_name='reply',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bpsapp.LocationReview'),
        ),
    ]
