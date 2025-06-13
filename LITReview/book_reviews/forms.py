from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image"
        }

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label="Note"
        )
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
        labels = {
            "ticket": "Billet",
            "headline": "Titre",
            "body": "Texte"
        }
