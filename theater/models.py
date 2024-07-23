
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from datetime import datetime, date
from django.db.models.fields import BooleanField
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    is_admin = BooleanField(default=False)

    def serialize(self):
        return {
            "username": self.username,
            "is_admin": self.is_admin
        }

    def __str__(self):
        return f'{self.username}, admin ({self.is_admin})'

class Film(models.Model):
    title = models.CharField(max_length=64)
    poster = models.TextField()
    director = models.CharField(max_length=64)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=64)
    main_cast = models.CharField(max_length=64)
    imdb_rating = models.CharField(max_length=64)
    plot = models.CharField(max_length=500, blank=True)
    reserved_seats_amount = models.IntegerField(default=0)
    seats_available = models.IntegerField(default=48)
    reserved_seats = models.TextField(null=True, blank=True, default="")
    date_pub = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)

    def serialize(self):
        return {
            "title": self.title,
            "poster": self.poster,
            "director": self.director,
            "year": self.year,
            "genre": self.genre,
            "main_cast": self.main_cast,
            "imdb_rating": self.imdb_rating,
            "plot": self.plot,
            "reserved_seats_amount": self.reserved_seats_amount,
            "seats_available": self.seats_available,
            "reserved_seats": self.reserved_seats,
            "date_publication": self.date_pub.strftime("%b %d %Y, %I:%M %p")
        }
    
    def __str__(self):
        return f'{self.title} directed by {self.director}'

class Reservation(models.Model):
    reserver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booked", blank=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="reservations", blank=True, default="")
    seats_number = models.TextField(default="") # The seats_number attribute is represented as a string of numbers that each represent a seat within the theater. These numbers were assgined by the seatsIndex variable in the front-end. That's why the seats dictionary was created in views.py.
    seats_code = models.TextField(default="") # Since each seat is also represented by combination of a letter and a number, we call this combination a code. For example, a seat code is "A1", "F8", etc...
    reservation_id = models.CharField(max_length=64, default="")
    date_reserved = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "reserver": self.reserver.username,
            "film": self.film.title,
            "seats_number": self.seats_number,
            "seats_code": self.seats_code,
            "reservation_id": self.reservation_id,
            "date_reserved": self.date_reserved.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f'{self.reserver.username} reserved seats {self.seats_code} ({self.seats_number}) for {self.film.title}'