from django.forms import ModelForm
from django import forms
from .models import Film

# Create your forms here.

class NewFilmForm(ModelForm):
    class Meta:
        model = Film
        widgets = {
            'poster': forms.HiddenInput(),
            'director': forms.HiddenInput(),
            'year': forms.HiddenInput(),
            'genre': forms.HiddenInput(),
            'main_cast': forms.HiddenInput(),
            'imdb_rating': forms.HiddenInput(),
            'plot': forms.HiddenInput(),
            'seats_sold': forms.HiddenInput(),
            'seats_available': forms.HiddenInput()
        }
        fields = [
            'title' 
        ]