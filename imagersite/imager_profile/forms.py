"""Forms for editing user and profile."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django import forms
from django.forms.widgets import PasswordInput


class UserForm(forms.ModelForm):
    """Build form for editing user info."""

    class Meta:
        """Assign to User and select fields."""

        model = User
        fields = []
