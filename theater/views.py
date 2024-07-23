
# Relevant imports

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Film, Reservation
from .forms import NewFilmForm

import json
import requests # This import is necessary to get the utilized API to work.

# Variables for paginator that represents the amount of films/reservations we want to see per page.
films_per_page = 5
reservations_per_page = 5

# Dicitionary that relates a seat code to a seat number (index).
seat_dict = {
    "A1": "0",
    "A2": "1",
    "A3": "2",
    "A4": "3",
    "A5": "4",
    "A6": "5",
    "A7": "6",
    "A8": "7",
    "B1": "8",
    "B2": "9",
    "B3": "10",
    "B4": "11",
    "B5": "12",
    "B6": "13",
    "B7": "14",
    "B8": "15",
    "C1": "16",
    "C2": "17",
    "C3": "18",
    "C4": "19",
    "C5": "20",
    "C6": "21",
    "C7": "22",
    "C8": "23",
    "D1": "24",
    "D2": "25",
    "D3": "26",
    "D4": "27",
    "D5": "28",
    "D6": "29",
    "D7": "30",
    "D8": "31",
    "E1": "32",
    "E2": "33",
    "E3": "34",
    "E4": "35",
    "E5": "36",
    "E6": "37",
    "E7": "38",
    "E8": "39",
    "F1": "40",
    "F2": "41",
    "F3": "42",
    "F4": "43",
    "F5": "44",
    "F6": "45",
    "F7": "46",
    "F8": "47",
}

# Function to render the index page.
def index(request):

    # Boolean to know whether the user is logged in or not.
    anon = False

    # Get films.
    films = Film.objects.all().order_by('-date_pub')

    # Create the paginator object and create variables to represent page numbers and the objects inside each page.
    paginator = Paginator(films, films_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user

    # Render the page differently depending on the anonimity of the user (logged in or not).
    if user.is_anonymous:
        anon = True
        return render(request, "theater/index.html", {
            "anon": anon,
            "page_obj": page_obj
        })
    else:
        return render(request, "theater/index.html", {
            "anon": anon,
            "page_obj": page_obj
        })

# Function that logs the user in.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "theater/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "theater/login.html")

# Function that logs the user out.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Function that registers a user into the app. It creates a User instance.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "theater/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "theater/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "theater/register.html")

# Function that runs when an admin user clicks on 'New film'.
def new_film(request):

    # Create a new form to allow the user to fill in the contents of the new post.
    form = NewFilmForm()

    # Render the page in which the form will be found. 
    return render(request, "theater/new_film.html", {
        "form": form
    })

# Function that allows a user to search a film within the database.
def search_film(request):

    # When the search button in the navbar is pressed
    if request.method == "POST":

        # We fetch what the user typed in
        searched = request.POST['searched']

        # We create three querysets, in case the user was searching a film by title, by its main cast or by its director.
        films_bytitle = Film.objects.filter(title__contains=searched).order_by('-date_pub')
        films_bymaincast = Film.objects.filter(main_cast__contains=searched).order_by('-date_pub')
        films_bydirector = Film.objects.filter(director__contains=searched).order_by('-date_pub')

        # Get a single queryset from all the possible ones.
        qs = [films_bytitle, films_bymaincast, films_bydirector]

        # Empty list to append film ids to. 
        ids = []

        # We look into all of the querysets.
        for q in qs:
            # For each film inside each queryset, we get its ID and append it to the ids list.
            for film in q:
                ids.append(film.id)
        
        # We get a single QuerySet of all the found films that match what the user searched, knowing that these will be the ones
        # whose id is in the ids list. These ids are unique, which guarantees no duplicate search results. 
        films = Film.objects.filter(id__in=ids).order_by('-date_pub')

        return render(request, 'theater/search_results.html', {
            'searched': searched,
            'films': films,
        })

# Function that renders a film's specific page.
def view_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    return render(request, "theater/film.html", {
        "film": film
    })

# Function that deletes a film from the database (only admins can do this).
def remove_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    film.delete()
    return HttpResponseRedirect(reverse("index"))

# Function that takes the consumer user to the reservation page, to allow him/her to select his/her seats.
def make_reservation(request, film_id):
    film = Film.objects.get(pk=film_id)

    return render(request, "theater/reservation_page.html", {
        "film": film
    })

# Function that takes the admin user to the reservation page, to allow him/her to view all available/occupied seats.
def view_reservations(request, film_id):
    film = Film.objects.get(pk=film_id)

    return render(request, "theater/reservation_page.html", {
        "film": film
    })

# Function that renders a page where a user can see all of his/her active reservations. 
def user_reservations(request, username):

    # Get the user from the database
    u = User.objects.get(username=username)

    # Get the user's reservations
    reservations = u.booked.all().order_by('-date_reserved')

    # Create the paginator object and create variables to represent page numbers and the objects inside each page.
    paginator = Paginator(reservations, reservations_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return a page that shows all the reservations that the user has made.
    return render(request, "theater/user_reservations.html", {
        "page_obj": page_obj
    })

# Function that allows a consumer user (not an admin) to delete only one of his/her own reservations.
def cancel_reservation_consumer(request, res_id):

    # Get the reservation by id
    res = Reservation.objects.get(pk=res_id)

    # Get the string that represents ALL the reserved seats for the film of that reservation and create a list from it.
    reserved_seats = res.film.reserved_seats
    reserved_seats_list = reserved_seats.split(',')

    # Get the string that represents this specific reservation's reserved seats and create a list from it.
    seats_number_res = res.seats_number
    seats_number_res_list = seats_number_res.split(',')

    # Remove those seats from the film's complete list of reserved seats. 
    for number in seats_number_res_list:
        if number in reserved_seats_list:
            reserved_seats_list.remove(number)

    # Convert the resulting list back to a comma-separated string.
    reserved_seats_new = ','.join(reserved_seats_list)
    
    # Update the film's attributes of reserved seats, reserved seats amount and available seats amount.
    res.film.reserved_seats = reserved_seats_new
    res.film.reserved_seats_amount -= len(seats_number_res_list)
    res.film.seats_available += len(seats_number_res_list)

    res.film.save()

    # Get the reserver's username to pass to reverse function.
    username = res.reserver.username

    # Finally, delete the reservation from the database.
    res.delete()

    # Redirect the user to his/her reservation's page.
    return HttpResponseRedirect(reverse('user_reservations', kwargs={"username": username}))
    
################################################ API functions ######################################################

# This function gets a movie from an API found at https://rapidapi.com/rapidapi/api/movie-database-imdb-alternative, and returns its
# attributes as a JSON object or Python dictionary depending on the request method.
def get_movie(request, movie_title):
    if request.method == "GET" or request.method == "POST":

        # Each movie in the database that these API fetches information from is identified by an imdbID. By doing a Search method call first,
        # we can get the imdbID of the movie.
        # First get the imdbID via a Search method. The API has two endpoints. One is By Search (this one), and the other is By ID or Title.
        url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

        # We search a movie by its title.
        querystring = {"s":movie_title,"page":"1","r":"json"}

        headers = {
            'x-rapidapi-key': "6d69fa9e62mshf0fa71841dc452ep1f366cjsn55d47751bf52", # This is the API key that was provided to me when I subscribed to this API.
            'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        res = json.loads(response.text)

        # If the searched movie is not found in the API database, render an error page.
        if ("Error" in res.keys()):
            return render(request, "theater/search_error.html", {
                "message": "The film you tried to create could not be found. Try typing in a more specific title."
            })

        # For each of the movies that the API returns when the search by movie title has completed, we are only interested in the one 
        # whose title matches the movie title that was typed in by the user. We get its imdbID and break the loop. 
        for i in range(len(res["Search"])):
            movie = res["Search"][i]
            title = movie["Title"]

            # If the movie imdbID is found, get it. If it is not found, render an error message.
            if title ==  movie_title or movie_title in title:
                movie_imdbID = movie["imdbID"]
                break
            else: 
                return render(request, "theater/search_error.html", {
                "message": "The film you tried to create could not be found. Try typing in a more specific title."
            })
        
        # Once we have the imdbID, we can pass on the attributes of the film we're looking for via another API call, this time using the other
        # endpoint called By ID or Title.
        querystring = {"i":movie_imdbID,"r":"json"}

        headers = {
            'x-rapidapi-key': "6d69fa9e62mshf0fa71841dc452ep1f366cjsn55d47751bf52", # Same API key.
            'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # The movie attributes are returned to us as a Python dictionary.
        movie_attrs = json.loads(response.text)
        
        # We may need these attributes as a JSON object (for the front-end), or as a dictionary (for the back-end).
        if request.method == "GET":
            return JsonResponse(movie_attrs)
        elif request.method == "POST":
            return movie_attrs

# This function allows to create a reservation instance and update the corresponding film's attributes. 
@csrf_exempt
def reserve(request, film_id):

    # Making reservations must be done via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST method required."}, status=400)

    # Extract data from the front end.
    data = json.loads(request.body)
    new_reserved_seats = data.get("reserved_seats")
    new_reserved_seats_codes = data.get("seat_codes")
    reservation_id = data.get("reservation_id")

    # Get the film and update its reserved seats
    film = Film.objects.get(pk=film_id)

    # If the film didn't previously have reserved seats, there's no need to append a comma to its strin attribute representing reserved seats.
    if (len(film.reserved_seats) == 0):
        film.reserved_seats = film.reserved_seats + new_reserved_seats
        film.save(update_fields=['reserved_seats'])
    else:
        film.reserved_seats = film.reserved_seats + "," + new_reserved_seats
        film.save(update_fields=['reserved_seats'])

    # Create a list from the string of seat codes.
    new_reserved_seats_codes_list = new_reserved_seats_codes.split(',')

    # For each code in the previously created list, get its corresponding number using the global dictionary declared at the top of this script,
    # and append it to the seats_number list.
    seats_number = []
    for code in new_reserved_seats_codes_list:
        number = seat_dict[code]
        seats_number.append(number)

    # Convert said list to a comma-separated string so that the reservation instance can be appropriately created.
    seats_number = ','.join(seats_number)

    # Create reservation object
    res = Reservation(reserver=request.user, film=film, seats_number=seats_number, seats_code=new_reserved_seats_codes, reservation_id=reservation_id)
    res.save()

    return JsonResponse({"message": "Reserved seats for " + str(film.title) + " updated."})

# Function that returns a JSON object representing a film's attributes. 
def film(request, film_id):

    film = Film.objects.get(pk=film_id)
    if request.method == "GET":
        return JsonResponse(film.serialize(), safe=False)

# This function allows to update a film's available and reserved amount of seats.
@csrf_exempt
def update_seats(request, film_id):

    # Query for requested film.
    try:
        film = Film.objects.get(pk=film_id)
    except Film.DoesNotExist:
        return JsonResponse({"error": "Film not found."}, status=404)

    # Update availabe/reserved seats amount.
    if request.method == "PUT":
        data = json.loads(request.body)
        film.reserved_seats_amount = data.get('reserved_amount')
        film.seats_available = data.get('available_amount')

        # Update database
        film.save(update_fields=['reserved_seats_amount'])
        film.save(update_fields=['seats_available'])
        film.save()

        return HttpResponse(status=204)

    # Update seats must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

# Function that allows the user to get all the reservations corresponding to a specific film, and return them as a JSON object. 
def get_reservations(request, film_id):

    if request.method == "GET":
        film = Film.objects.get(pk=film_id)
        reservations = Reservation.objects.filter(film=film)
        l = [res.serialize() for res in reservations]

        return JsonResponse(l, safe=False)

# Function that allows an admin user to cancel a reservation. Notice that this function is called from the front-end. 
@csrf_exempt
def cancel_reservation(request, res_id):

    if request.method == "POST":

        # Get the specific reservatino instance, get its reserved seats and create a list from it.
        res = Reservation.objects.get(pk=res_id)
        reserved_seats = res.film.reserved_seats
        reserved_seats_list = reserved_seats.split(',')

        # Extract data
        data = json.loads(request.body)
        seats_number_res = data.get("seats_number")

        # Create list from the seats_number list previosuly created.
        seats_number_res_list = seats_number_res.split(',')

        # Remove the wanted seats from the list of all reserved seats of that reservation. 
        for number in seats_number_res_list:
            if number in reserved_seats_list:
                reserved_seats_list.remove(number)

        # Get the updated list (with the removed seats) and convert it back to a comma-separated string.
        reserved_seats_new = ','.join(reserved_seats_list)

        # Update reserved/available seats in the database for the specific film of the reservation in question. 
        res.film.reserved_seats = reserved_seats_new
        res.film.reserved_seats_amount -= len(seats_number_res_list)
        res.film.seats_available += len(seats_number_res_list)

        reserved_seats_amount_new = res.film.reserved_seats_amount
        seats_available_new = res.film.seats_available

        res.film.save()
        
        # After saving all attributes, delete the reservation instance from the database. 
        res.delete()

    # Return the old and new seat numbers for the film corresponding to this reservation and the new amounts of available/reserved seats in a JSON object.
    return JsonResponse({"seats_number_res": seats_number_res, "reserved_seats_new": reserved_seats_new, "reserved_seats_amount_new": reserved_seats_amount_new, "seats_available_new": seats_available_new})


##################################### Functions that depend on calls to the API ###################################################

# Function that creates a new film. It runs when the user submits the 'New film' form.
def create_film(request):

    if request.method == "POST":

        # Get the content of the form and save it. Return the user to the index page. 
        form = NewFilmForm(request.POST)
        if form.is_valid():
            title = form.instance.title
            # We call the function that makes a call to the API to get the film's attributes. 
            movie = get_movie(request, title)
            try:
                form.instance.poster = movie["Poster"]
                form.instance.director = movie["Director"]
                form.instance.year = movie["Year"]
                form.instance.genre = movie["Genre"]
                form.instance.main_cast = movie["Actors"]
                form.instance.imdb_rating = movie["imdbRating"]
                form.instance.plot = movie["Plot"]
                form.save()
                return HttpResponseRedirect(reverse("index"))
            except KeyError:
                message = "The film you tried to create could not be found. Try typing in a more specific title."
                return render(request, "theater/search_error.html", {
                    "message": message
                })