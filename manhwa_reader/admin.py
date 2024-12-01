# manhwa_reader/admin.py
from django.contrib import admin
from .models import *

@admin.register(Manhwa)
class ManhwaAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('genres',)
    search_fields = ('title',)
    filter_horizontal = ('genres',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Chapter)
admin.site.register(UserProfile)
admin.site.register(Image)
