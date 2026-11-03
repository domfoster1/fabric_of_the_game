"""
Database models for football shirt collections.
"""

from django.db import models


class Shirt(models.Model):
    """Store information about a football shirt."""

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='shirts'
    )

    team = models.CharField(max_length=100)
    season = models.CharField(max_length=30)

    shirt_type = models.CharField(
        max_length=20,
        choices=[
            ('Home', 'Home'),
            ('Away', 'Away'),
            ('Third', 'Third'),
            ('Goalkeeper', 'Goalkeeper'),
            ('Training', 'Training'),
            ('Other', 'Other'),
        ]
    )

    issue = models.CharField(
        max_length=20,
        choices=[
            ('Fan', 'Fan Issue'),
            ('Player', 'Player Issue'),
            ('Match Worn', 'Match Worn'),
        ]
    )

    size = models.CharField(
        max_length=10,
        choices=[
            ('Kids', 'Kids'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', '2XL'),
            ('XXXL', '3XL'),
            ('Other', 'Other'),
        ]
    )

    condition = models.CharField(
        max_length=30,
        choices=[
            ('New with tags', 'Brand new with tags'),
            ('New without tags', 'Brand new without tags'),
            ('Excellent', 'Excellent'),
            ('Very good', 'Very good'),
            ('Good', 'Good'),
            ('Fair', 'Fair'),
        ]
    )

    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShirtImage(models.Model):
    """Store photographs of a football shirt."""

    image = models.ImageField(upload_to='shirt_images/')
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)