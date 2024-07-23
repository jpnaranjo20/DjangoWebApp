# Generated by Django 3.1.4 on 2021-07-03 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0013_auto_20210702_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserver',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='booked', to=settings.AUTH_USER_MODEL),
        ),
    ]
