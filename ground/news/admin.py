from django.contrib import admin

# Register your models here.
from .models import Tweets, StreamState, StreamFilters

admin.site.register(Tweets)
admin.site.register(StreamState)
admin.site.register(StreamFilters)

