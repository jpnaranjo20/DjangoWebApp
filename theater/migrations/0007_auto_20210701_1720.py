# Generated by Django 3.1.4 on 2021-07-01 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0006_auto_20210628_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='plot',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='film',
            name='seats_available',
            field=models.IntegerField(default=48),
        ),
    ]
