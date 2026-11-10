"""
Views for the My Collection page.
"""
from email.mime import image
from urllib import request

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ShirtForm, ShirtImageForm, RegistrationForm, CommentForm
from .forms import ShirtForm
from .models import Shirt, ShirtImage, Comment


@login_required
def my_collection(request):
    """Display the user's shirt collection and filter shirts."""

    shirts = Shirt.objects.filter(owner=request.user).order_by('-date_added')

    # Get the search and filter values
    team = request.GET.get('team')
    season = request.GET.get('season')
    manufacturer = request.GET.get('manufacturer')
    country = request.GET.get('country')
    league = request.GET.get('league')
    player = request.GET.get('player')

    # Filter the user's shirts using the values entered
    if team:
        shirts = shirts.filter(team__icontains=team)

    if season:
        shirts = shirts.filter(season__icontains=season)

    if manufacturer:
        shirts = shirts.filter(manufacturer=manufacturer)

    if country:
        shirts = shirts.filter(country=country)

    if league:
        shirts = shirts.filter(league=league)

    if player:
        shirts = shirts.filter(player_name__icontains=player)

    return render(request, 'my_collection/collection.html', {
        'shirts': shirts,
        'manufacturer_choices': Shirt._meta.get_field('manufacturer').choices,
        'country_choices': Shirt._meta.get_field('country').choices,
        'league_choices': Shirt._meta.get_field('league').choices,
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


def user_collection(request, username):
    """Display and filter a user's public shirt collection."""

    collection_owner = get_object_or_404(User, username=username)

    shirts = Shirt.objects.filter(
        owner=collection_owner
    ).order_by('-date_added')

    # Get the search and filter values
    team = request.GET.get('team')
    season = request.GET.get('season')
    manufacturer = request.GET.get('manufacturer')
    country = request.GET.get('country')
    league = request.GET.get('league')
    player = request.GET.get('player')

    # Filter this user's shirts using the values entered
    if team:
        shirts = shirts.filter(team__icontains=team)

    if season:
        shirts = shirts.filter(season__icontains=season)

    if manufacturer:
        shirts = shirts.filter(manufacturer=manufacturer)

    if country:
        shirts = shirts.filter(country=country)

    if league:
        shirts = shirts.filter(league=league)

    if player:
        shirts = shirts.filter(player_name__icontains=player)

    return render(request, 'my_collection/user_collection.html', {
        'collection_owner': collection_owner,
        'shirts': shirts,
        'manufacturer_choices': Shirt._meta.get_field('manufacturer').choices,
        'country_choices': Shirt._meta.get_field('country').choices,
        'league_choices': Shirt._meta.get_field('league').choices,
    })


@login_required
def add_comment(request, shirt_id):
    """Allow a logged-in user to comment on a shirt."""

    shirt = get_object_or_404(Shirt, id=shirt_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.shirt = shirt
            comment.owner = request.user
            comment.save()

    if request.GET.get('next') == 'home':
        return redirect('home')

    return redirect('user_collection', username=shirt.owner.username)

@login_required
def edit_comment(request, comment_id):
    """Allow a user to edit their own comment."""

    comment = get_object_or_404(Comment, id=comment_id, owner=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('user_collection', username=comment.shirt.owner.username)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'my_collection/edit_comment.html', {
        'form': form
    })


@login_required
def delete_comment(request, comment_id):
    """Allow a user to delete their own comment."""

    comment = get_object_or_404(Comment, id=comment_id, owner=request.user)

    if request.method == 'POST':
        username = comment.shirt.owner.username
        comment.delete()
        return redirect('user_collection', username=username)

    return render(request, 'my_collection/delete_comment.html', {
        'comment': comment
    })

