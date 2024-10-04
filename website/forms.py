from .models import *
from django import forms

class NewTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['book', 'description', 'image']
        labels = {
            'book': 'Titre du livre',
            'description': 'Description',
            'image': 'Image'
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'headline', 'rating', 'body' ]
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(6)])
        }

class CombinedTicketReviewForm(forms.Form):
    # Champs pour le ticket
    ticket_book = forms.CharField(max_length=128, label='Titre du livre')
    ticket_description = forms.CharField(widget=forms.Textarea, required=False, label='Description du livre')
    ticket_image = forms.ImageField(required=False, label='Image du livre')
    
    # Champs pour la review
    headline = forms.CharField(max_length=128, label='Titre de la critique')
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(6)], widget=forms.RadioSelect, label='Note')
    body = forms.CharField(widget=forms.Textarea, label='Votre critique')        