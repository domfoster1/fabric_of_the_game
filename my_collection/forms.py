"""
Shirt forms.
"""

from django import forms
from .models import Shirt

class ShirtForm(forms.ModelForm):
    """Form for adding a football shirt."""

    class Meta:
        model = Shirt
        exclude = ['owner', 'date_added']