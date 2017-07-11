"""Forms for editing user and profile."""
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from django import forms


class UserForm(forms.ModelForm):
    """Build form for editing user info."""

    class Meta:
        """Assign to User and select fields."""

        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


# class ImagerProfileForm(forms.ModelForm):
#     """Build form for editing profile info."""

#     class Meta:
#         """Assign to ImagerProfile and select fields."""

#         model = ImagerProfile
#         exclude = ['user']
