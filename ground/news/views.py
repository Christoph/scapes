# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Tweet


def index(request):
    tweet_list = Tweet.objects.order_by('-tweet_id')[:2]

    context = {
        'tweet_list': tweet_list,
    }

    return render(request, 'news/index.html', context)


def overview(request):
    return HttpResponse("Twitter Stream")


def tweet(request, tweetid):
    try:
        entry = Tweet.objects.get(tweet_id=tweetid)
    except Tweet.DoesNotExist:
        raise Http404("Tweet does not exist")
    return render(request, 'news/tweet.html', {'tweet': entry})
