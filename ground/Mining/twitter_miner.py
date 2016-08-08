# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import re
from ast import literal_eval

from news.models import StreamFilters, StreamState, Tweet


# Save Tweets into the db
class StdOutListener(StreamListener):

    def on_data(self, data):
        parsed = json.loads(data)

        # m = re.search(r'(media_url": ")(.*)"', data)
        m = re.search(r'(media_url).*(http:.*?\.jpg)', data)

        print("regex")

        if m is not None:
            print(m.groups())
            print(re.sub(r'\\\\\\\\', "", m.group(2)))

        t = Tweet.create_from_json(parsed)
        t.save()

        return True

    def on_error(self, status):
        print(status)
        streamstate = StreamState.objects.get(pk=3)

        streamstate.is_active = False
        streamstate.save()

        return False


class Twitter:

    def __init__(self):
        self.api = []
        self.stream = []
        self.streaming = False
        self.lastpull = Tweet.objects.order_by("-created_at")[0].created_at


    def get_new_tweets(self):
        new = Tweet.objects.filter(created_at__gt=self.lastpull)

        if len(new) > 0:
            self.lastpull = new.order_by("-created_at")[0].created_at

        return new


    def connect_twitter(self):
        streamstate = StreamState.objects.get(pk=3)
        listener = StdOutListener()

        auth = OAuthHandler(streamstate.c_key, streamstate.c_secret)
        auth.set_access_token(streamstate.a_token, streamstate.a_secret)

        # Create handlers
        self.api = tweepy.API(auth)
        self.stream = Stream(auth, listener)
        print("Authenticated")


    def connect_to_stream(self, choosen):
        streamstate = StreamState.objects.get(pk=3)

        # Filter by track and language
        if not self.streaming:
            if choosen == 1:
                filters = StreamFilters.objects.get(pk=choosen)

                tracks = literal_eval(filters.tracks)
                languages = literal_eval(filters.languages)

                self.stream.filter(track=tracks, languages=languages, async=True)
                print("Streaming")

                streamstate.is_active = True
                streamstate.save()
                self.streaming = True

            # Filter by location and language
            if choosen == 2:
                filters = StreamFilters.objects.get(pk=choosen)

                language = literal_eval(filters.languages)
                locations = literal_eval(filters.locations)

                self.stream.filter(locations=locations, languages=language, async=True)
                print("Streaming")

                streamstate.is_active = True
                streamstate.save()
                self.streaming = True


    def disconnet_from_stream(self):
        self.stream.disconnect()
        print("Stopped Streaming")

        streamstate = StreamState.objects.get(pk=3)

        streamstate.is_active = False
        streamstate.save()

        self.streaming = False




