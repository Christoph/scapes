from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the news index.")


def overview(request):
    return HttpResponse("Twitter Stream")


def tweet(request, tweet_id):
    response = "Tweet ID %s."
    return HttpResponse(response % tweet_id)


