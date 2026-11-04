from django.contrib import admin
from .models import Shirt, ShirtImage, Comment

admin.site.register(Shirt)
admin.site.register(ShirtImage)
admin.site.register(Comment)