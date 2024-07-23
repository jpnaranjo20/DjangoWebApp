# Generated by Django 3.1.4 on 2021-07-02 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0008_auto_20210701_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='film',
        ),
        migrations.AddField(
            model_name='reservation',
            name='film',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='theater.film'),
        ),
    ]
