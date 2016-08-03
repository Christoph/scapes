# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Tweet
from Mining.twitter_miner import Twitter

from django.conf import settings



def index(request):
    tweet_list = Tweet.objects.order_by('-tweet_id')[:2]

    context = {
        'tweet_list': tweet_list,
    }

    return render(request, 'news/index.html', context)


def overview(request):
    twitter = Twitter(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    twitter.connect_twitter()
    twitter.connect_to_stream()

    return HttpResponse("Twitter Stream")


def tweet(request, tweetid):
    entry = get_object_or_404(Tweet, tweet_id=tweetid)
    return render(request, 'news/tweet.html', {'tweet': entry})
