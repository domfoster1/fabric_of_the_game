"""
Views for the My Collection page.
"""
from email.mime import image
from urllib import request

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShirtForm, ShirtImageForm, RegistrationForm
from .forms import ShirtForm
from .models import Shirt, ShirtImage


@login_required
def my_collection(request):
    """Display the user's shirt collection."""

    shirts = Shirt.objects.filter(owner=request.user)

    return render(request, 'my_collection/collection.html', {
        'shirts': shirts
    })


@login_required
def add_shirt(request):
    """Allow a user to add a football shirt."""

    if request.method == 'POST':
        form = ShirtForm(request.POST, request.FILES)

        if form.is_valid():
            shirt = form.save(commit=False)
            shirt.owner = request.user
            shirt.save()

            for image in request.FILES.getlist('images'):
                ShirtImage.objects.create(
                    shirt=shirt,
                    image=image
                )

            return redirect('my_collection')

    else:
        form = ShirtForm()

    return render(request, 'my_collection/add_shirt.html', {'form': form})

@login_required
def edit_shirt(request, shirt_id):
    """Allow a user to edit their own shirt."""

    shirt = get_object_or_404(Shirt, id=shirt_id, owner=request.user)

    if request.method == 'POST':
        form = ShirtForm(request.POST, instance=shirt)

        if form.is_valid():
            form.save()
            return redirect('my_collection')

    else:
        form = ShirtForm(instance=shirt)

    return render(request, 'my_collection/edit_shirt.html', {'form': form})

@login_required
def delete_shirt(request, shirt_id):
    """Allow a user to delete their own shirt."""

    shirt = get_object_or_404(Shirt, id=shirt_id, owner=request.user)

    if request.method == 'POST':
        shirt.delete()
        return redirect('my_collection')

    return render(request, 'my_collection/delete_shirt.html', {'shirt': shirt})

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