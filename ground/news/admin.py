from django.contrib import admin

# Register your models here.
from .models import Tweet, StreamState, StreamFilters

admin.site.register(Tweet)
admin.site.register(StreamState)
admin.site.register(StreamFilters)

