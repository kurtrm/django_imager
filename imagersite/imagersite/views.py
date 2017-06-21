"""Project-level views."""
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def home_view(request):
    """View for the home page."""
    return render(
        request,
        'imagersite/home.html',
        context={'content': 'cake'}
    )


def account_view(request):
    """View for the registration page."""
    return render(request, 'registration/account.html')
