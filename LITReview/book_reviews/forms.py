from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect
        )
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
