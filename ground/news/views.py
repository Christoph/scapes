# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, modelformset_factory
from django.urls import reverse

from .models import Tweet, StreamFilters
from Mining.twitter_miner import Twitter


# Create twitter miner instance
twitter = Twitter()
twitter.connect_twitter()


class FilterForm(ModelForm):
    class Meta:
        model = StreamFilters
        fields = ['tracks', 'locations', 'languages']



def index(request):
    tweet_list = Tweet.objects.order_by('-tweet_id')[:2]

    context = {
        'tweet_list': tweet_list,
    }

    twitter.disconnet_from_stream()
    print("disconnected")
    return render(request, 'news/index.html', context)


def overview(request):
    twitter.connect_to_stream(2)
    print("connected")

    return HttpResponse("Twitter Stream")


def tweet(request, tweetid):
    entry = get_object_or_404(Tweet, tweet_id=tweetid)
    return render(request, 'news/tweet.html', {'tweet': entry})


def filterView(request):
    form = modelformset_factory(StreamFilters, form=FilterForm)

    if request.method == 'POST':
        formset = form(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('news:index'))
    else:
        formset = form()

    return render(request, 'news/filter.html', {'formset': formset})







