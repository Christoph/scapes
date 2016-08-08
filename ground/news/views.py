# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import ModelForm, modelformset_factory
from django.urls import reverse

from .models import Tweets, StreamFilters
from Mining.twitter_miner import Twitter


# Create twitter miner instance
twitter = Twitter()
twitter.connect_twitter()


class FilterForm(ModelForm):
    class Meta:
        model = StreamFilters
        fields = ['tracks', 'locations', 'languages']


def index(request):
    tweet_list = Tweets.objects.order_by('-created_at')[:20]

    context = {
        'tweet_list': tweet_list,
    }

    twitter.disconnet_from_stream()
    return render(request, 'news/index.html', context)


def overview(request):

    # Load data with ajax
    if request.method == 'POST':
        # post_text = request.POST.get('text')
        # print(post_text)

        if not twitter.streaming:
            twitter.connect_to_stream(1)

        new = twitter.get_new_tweets()

        data = [{'tweet_id': item.tweet_id,'text': item.text, 'user_location': item.user_location} for item in new]

        return JsonResponse({"list": data})

    # Load page
    return render(request, 'news/stream.html')


def tweet(request, tweetid):
    entry = get_object_or_404(Tweets, tweet_id=tweetid)
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







