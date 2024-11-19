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

class FollowUserForm(forms.ModelForm):
    follows = forms.CharField(label="Nom d'utilisateur à suivre")

    class Meta:
        model = models.UserFollows
        fields = []