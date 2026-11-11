"""
Shirt forms.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Shirt, ShirtImage, Comment


class ShirtForm(forms.ModelForm):
    """Form for adding a football shirt."""

    class Meta:
        model = Shirt
        exclude = ['owner', 'date_added']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Give the fields clearer names
        labels = {
            'team': 'Team',
            'season': 'Season',
            'shirt_type': 'Shirt Type',
            'manufacturer': 'Manufacturer',
            'country': 'Country',
            'league': 'League',
            'issue': 'Shirt Issue',
            'condition': 'Condition',
            'size': 'Size',
            'player_name': 'Player Name (optional)',
            'shirt_number': 'Shirt Number (optional)',
            'description': 'Tell us about your shirt',
        }

        # Add styling and helpful placeholders to the fields
        placeholders = {
            'team': 'Enter the team name',
            'season': 'e.g. 2024/25',
            'player_name': 'Enter the player name',
            'shirt_number': 'Enter the shirt number',
            'description': 'Share the story behind your shirt...',
        }

        for field_name, field in self.fields.items():

            # Update the field label
            if field_name in labels:
                field.label = labels[field_name]

            # Style dropdowns and input boxes
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

            # Add placeholder text where needed
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

            # Make the description box larger
            if field_name == 'description':
                field.widget.attrs.update({'rows': 4})


class ShirtImageForm(forms.ModelForm):
    """Form for uploading a shirt photo."""

    class Meta:
        model = ShirtImage
        fields = ['image']


class RegistrationForm(UserCreationForm):
    """Form for creating a new user account."""

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        """Check that the email address is not already in use."""

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email address is already registered.'
                    )

        return email


class CommentForm(forms.ModelForm):
    """Form for adding a comment to a shirt."""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write a comment...',
                'rows': 3
            })
        }
