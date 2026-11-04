"""
Views for the homepage.
"""

from django.shortcuts import render
from my_collection.models import Shirt


def home(request):
    """Display the homepage and all uploaded shirts."""

    shirts = Shirt.objects.all().order_by('-date_added')

    return render(request, 'homepage/home.html', {
        'shirts': shirts
    })