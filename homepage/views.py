"""
Views for the homepage.
"""

from django.shortcuts import render
from my_collection.models import Shirt


def home(request):
    """Display the homepage and filter shirts."""

    shirts = Shirt.objects.all().order_by('-date_added')

    # Get the search and filter values
    team = request.GET.get('team')
    season = request.GET.get('season')
    manufacturer = request.GET.get('manufacturer')
    country = request.GET.get('country')
    league = request.GET.get('league')
    player = request.GET.get('player')

    # Filter shirts using the values entered
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

    return render(request, 'homepage/home.html', {
        'shirts': shirts,
        'manufacturer_choices': Shirt._meta.get_field('manufacturer').choices,
        'country_choices': Shirt._meta.get_field('country').choices,
        'league_choices': Shirt._meta.get_field('league').choices,
    })
    