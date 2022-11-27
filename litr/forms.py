from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'description': forms.Textarea(),
        }
        labels = {
            'title': "Titre",
            'description': "Description"
        }


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        CHOICES = [(i, i) for i in range(6)]
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Titre'}),
            'rating': forms.RadioSelect(choices=CHOICES),
        }
        labels = {
            'headline': "Titre",
            'rating': "Note",
            'body': "Commentaire"
        }


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.request_user = kwargs.pop("request_user")
            self.former_followed_user = kwargs.pop("former_followed_user")
        super(FollowUsersForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

    def clean_followed_user(self):
        data = self.cleaned_data["followed_user"]
        if self.request_user:
            if self.request_user == data:
                raise ValidationError("Vous ne pouvez vous suivre vous-même!", code="invalid")
            if self.former_followed_user.filter(followed_user=data).exists():
                raise ValidationError("Abonné déja suivi!", code="invalid")
        return data
