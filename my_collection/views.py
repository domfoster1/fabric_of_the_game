"""
Views for the My Collection page.
"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ShirtForm, RegistrationForm
from .forms import ShirtForm


def my_collection(request):
    """Display the user's shirt collection."""
    return render(request, 'my_collection/collection.html')


@login_required
def add_shirt(request):
    """Allow a user to add a football shirt."""

    if request.method == 'POST':
        form = ShirtForm(request.POST)

        if form.is_valid():
            shirt = form.save(commit=False)
            shirt.owner = request.user
            shirt.save()

            return redirect('my_collection')

    else:
        form = ShirtForm()

    return render(request, 'my_collection/add_shirt.html', {'form': form})


def register(request):
    """Allow a new user to create an account."""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})