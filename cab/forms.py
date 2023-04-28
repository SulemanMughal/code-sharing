from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Snippet,
    Language
)

# ? Current Active User Model
User = get_user_model()


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ['author']