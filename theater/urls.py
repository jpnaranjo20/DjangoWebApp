
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_film", views.new_film, name="new_film"),
    path("create_film", views.create_film, name="create_film"),
    path("view_film/<int:film_id>", views.view_film, name="view_film"),
    path("remove_film/<int:film_id>", views.remove_film, name="remove_film"),
    path("make_reservation/<int:film_id>", views.make_reservation, name="make_reservation"),
    path("view_reservations/<int:film_id>", views.view_reservations, name="view_reservations"),
    path("user_reservations/<str:username>", views.user_reservations, name="user_reservations"),
    path("cancel_reservation_consumer/<int:res_id>", views.cancel_reservation_consumer, name="cancel_reservation_consumer"),
    path("search", views.search_film, name="search"),

    # API routes
    path("get_movie/<str:movie_title>", views.get_movie, name="get_movie"),
    path("reserve/<int:film_id>", views.reserve, name="reserve"),
    path("film/<int:film_id>", views.film, name="film"),
    path("update_seats/<int:film_id>", views.update_seats, name="update_seats"),
    path("get_reservations/<int:film_id>", views.get_reservations, name="get_reservations"),
    path("cancel_reservation/<int:res_id>", views.cancel_reservation, name="cancel_reservation")
]
