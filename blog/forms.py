from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    class Meta:
        model=models.Review
        fields=['headline', 'body', 'rating']
        labels={
            'headline':'Titre',
            'body': 'Commentaires',
            'rating':'Note'
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model=models.Ticket
        fields=['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image'
        }

class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur à suivre", max_length=150)