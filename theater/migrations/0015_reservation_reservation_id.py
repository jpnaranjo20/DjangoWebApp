# Generated by Django 3.1.4 on 2021-07-04 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0014_auto_20210702_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_id',
            field=models.TextField(default=''),
        ),
    ]
