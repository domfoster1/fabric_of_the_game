from django.contrib import admin
from .models import Shirt, ShirtImage, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Manage comments and their approval status."""

    list_display = ('owner', 'shirt', 'approved', 'date_added')
    list_filter = ('approved', 'date_added')
    list_editable = ('approved',)


admin.site.register(Shirt)
admin.site.register(ShirtImage)
