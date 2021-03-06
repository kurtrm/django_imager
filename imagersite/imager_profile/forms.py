"""Forms for editing user and profile."""
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    """Build form for editing user info."""

    class Meta:
        """Assign to User and select fields."""

        model = User
        fields = []
