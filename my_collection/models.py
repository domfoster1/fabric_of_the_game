from django.db import models

# Create your models here.

class Shirt(models.Model):
"""Store information about a football shirt."""   

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='shirts'
    )

team = models.CharField(max_length=100)
season = models.CharField(max_length=30)
shirt_type = models.CharField(max_length=20)
issue = models.CharField(max_length=20)
size = models.CharField(max_length=10)
condition = models.CharField(max_length=30)
description = models.TextField(blank=True)
date_added = models.DateTimeField(auto_now_add=True)