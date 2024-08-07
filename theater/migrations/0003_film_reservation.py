# Generated by Django 3.1.4 on 2021-06-26 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0002_user_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('poster', models.TextField()),
                ('director', models.CharField(max_length=64)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('genre', models.CharField(max_length=64)),
                ('main_cast', models.CharField(max_length=64)),
                ('imdb_rating', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ManyToManyField(blank=True, related_name='reservations', to='theater.Film')),
                ('reserver', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
