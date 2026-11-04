"""
Database models for football shirt collections.
"""

from django.db import models
from django_countries import countries
from django_countries.fields import CountryField
from django.db.models.signals import post_delete
from django.dispatch import receiver

COUNTRIES = [
    ('GB-ENG', 'England'),
    ('GB-SCT', 'Scotland'),
    ('GB-WLS', 'Wales'),
    ('GB-NIR', 'Northern Ireland'),
] + [
    (code, name)
    for code, name in countries
    if code != 'GB'
]

LEAGUES = [
    ('Premier League', 'Premier League'),
    ('Championship', 'Championship'),
    ('League One', 'League One'),
    ('League Two', 'League Two'),
    ('Scottish Premiership', 'Scottish Premiership'),
    ('Scottish Championship', 'Scottish Championship'),
    ('Cymru Premier', 'Cymru Premier'),
    ('NIFL Premiership', 'NIFL Premiership'),
    ('La Liga', 'La Liga'),
    ('Bundesliga', 'Bundesliga'),
    ('Serie A', 'Serie A'),
    ('Ligue 1', 'Ligue 1'),
    ('MLS', 'MLS'),
    ('Brazilian Serie A', 'Brazilian Serie A'),
    ('J1 League', 'J1 League'),
    ('J2 League', 'J2 League'),
    ('J3 League', 'J3 League'),
    ('Other', 'Other'),
]

class Shirt(models.Model):
    """Store information about a football shirt."""

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='shirts'
    )

    team = models.CharField(max_length=100)
    season = models.CharField(max_length=30)

    manufacturer = models.CharField(
    max_length=30,
    choices=[
        ('Adidas', 'Adidas'),
        ('Nike', 'Nike'),
        ('Puma', 'Puma'),
        ('Umbro', 'Umbro'),
        ('New Balance', 'New Balance'),
        ('Kappa', 'Kappa'),
        ('Macron', 'Macron'),
        ('Hummel', 'Hummel'),
        ('Castore', 'Castore'),
        ('Other', 'Other'),
    ]
    )

    country = models.CharField(
    max_length=100,
    choices=COUNTRIES,
    )

    league = models.CharField(
    max_length=50,
    choices=LEAGUES,
    )

    player_name = models.CharField(max_length=100, blank=True)
    shirt_number = models.PositiveSmallIntegerField(null=True, blank=True)

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

    def __str__(self):
        """Show the team and season of the shirt."""
        return f"{self.team} - {self.season}"

class ShirtImage(models.Model):
    """Store photographs of a football shirt."""

    image = models.ImageField(upload_to='shirt_images/')
    shirt = models.ForeignKey(Shirt, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """Show which shirt the photograph belongs to."""
        return f"Photo of {self.shirt}"

# Delete the photograph file when its database record is deleted
@receiver(post_delete, sender=ShirtImage)
def delete_shirt_image_file(sender, instance, **kwargs):

    """Delete the uploaded photograph from storage."""

    if instance.image:
        instance.image.delete(save=False)   

class Comment(models.Model):
    """Store comments left on football shirts."""

    shirt = models.ForeignKey(
        Shirt,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='shirt_comments'
    )

    content = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Show who wrote the comment."""
        return f"Comment by {self.owner} on {self.shirt}"