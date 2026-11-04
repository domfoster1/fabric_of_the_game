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

    def clean_email(self):
        """Check that the email address is not already in use."""

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')

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