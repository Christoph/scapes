# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Tweet


def index(request):
    tweet_list = Tweet.objects.order_by('-tweet_id')[:2]
    template = loader.get_template('news/index.html')

    context = {
        'tweet_list': tweet_list,
    }

    return HttpResponse(template.render(context, request))


def overview(request):
    return HttpResponse("Twitter Stream")


def tweet(request, tweet_id):
    response = "Tweet ID %s."
    return HttpResponse(response % tweet_id)
