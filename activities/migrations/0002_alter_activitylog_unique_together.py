# Generated by Django 5.0.2 on 2025-03-07 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='activitylog',
            unique_together=set(),
        ),
    ]
