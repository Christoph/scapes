from django.db import models
from datetime import datetime
from django.utils import timezone
from email._parseaddr import parsedate
import re


def parse_datetime(string):
    return datetime(*(parsedate(string)[:6]), tzinfo=timezone.utc)


class StreamFilters(models.Model):
    tracks = models.CharField(max_length=200, blank=True, null=True)
    locations = models.CharField(max_length=200, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if len(self.tracks) > 0:
            return self.tracks
        else:
            return self.locations


class StreamState(models.Model):
    TRACK_FILTER = "TrackFilter"
    LOCATION_FILTER = "LocationFilter"
    # State
    is_active = models.BooleanField(default=False)

    # Login
    c_key = models.CharField(max_length=100)
    c_secret = models.CharField(max_length=100)
    a_token = models.CharField(max_length=100)
    a_secret = models.CharField(max_length=100)

    def __str__(self):
        return "State"


# Create your models here.
class Tweets(models.Model):
    # Basic tweet info
    tweet_id = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    truncated = models.BooleanField(default=False)
    lang = models.CharField(max_length=9, null=True, blank=True, default=None)

    # Basic user info
    user_id = models.BigIntegerField()
    user_screen_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_verified = models.BooleanField(default=False)
    user_location = models.CharField(max_length=150, null=True, blank=True, default=None)

    # Timing parameters
    created_at = models.DateTimeField(db_index=True)  # should be UTC
    user_utc_offset = models.IntegerField(null=True, blank=True, default=None)
    user_time_zone = models.CharField(max_length=150, null=True, blank=True, default=None)

    # none, low, or medium
    filter_level = models.CharField(max_length=6, null=True, blank=True, default=None)

    # Place
    place_name = models.CharField(max_length=100, null=True, blank=True)
    place_type = models.CharField(max_length=100, null=True, blank=True)
    place_country = models.CharField(max_length=100, null=True, blank=True)
    place_full_name = models.CharField(max_length=100, null=True, blank=True)

    # Entities
    media_url = models.CharField(max_length=150, null=True, blank=True)
    urls = models.CharField(max_length=250, null=True, blank=True)
    hashtags = models.CharField(max_length=150, null=True, blank=True)

    # Engagement - not likely to be very useful for streamed tweets but whatever
    favorite_count = models.PositiveIntegerField(null=True, blank=True)
    retweet_count = models.PositiveIntegerField(null=True, blank=True)
    user_followers_count = models.PositiveIntegerField(null=True, blank=True)
    user_friends_count = models.PositiveIntegerField(null=True, blank=True)

    # Relation to other tweets
    in_reply_to_status_id = models.BigIntegerField(null=True, blank=True, default=None)
    retweeted_status_id = models.BigIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.text

    def is_retweet(self):
        return self.retweeted_status_id is not None

    @classmethod
    def create_from_json(cls, raw):

        # Prefixes
        user = raw['user']
        place = raw['place']

        # Set retweeted status
        retweeted_status = raw.get('retweeted_status')
        if retweeted_status is None:
            retweeted_status = {'id': None}
            retweet = raw
            entitie = raw['entities']
        else:
            retweet = raw["retweeted_status"]
            entitie = raw["retweeted_status"]['entities']

        # Set place
        places = [None, None, None, None]
        if raw.get("place"):
            if place.get('name'):
                places[0] = place['name']
            if place.get('full_name'):
                places[0] = place['full_name']
            if place.get('type'):
                places[0] = place['type']
            if place.get('country'):
                places[0] = place['country']

        # Set entities
        entities = {"media": "", "urls": "", "hashtags": ""}
        if raw.get("entities"):
            if entitie.get('media'):
                for entry in entitie['media']:
                    entities['media'] = entities['media'] + " " + entry['media_url']
                entities['media'] = re.sub(r'\\\\', "", entities['media'].strip())

            if entitie.get('urls'):
                for entry in entitie['urls']:
                    entities['urls'] = entities['urls'] + " " + entry['expanded_url']
                entities['urls'] = re.sub(r'\\\\', "", entities['urls'].strip())

            if entitie.get('hashtags'):
                for entry in entitie['hashtags']:
                    entities['hashtags'] = entities['hashtags'] + "," + entry['text']
                entities['hashtags'] = entities['hashtags'].strip()

        # Replace negative counts with None to indicate missing data
        counts = {
            'favorite_count': raw.get('favorite_count'),
            'retweet_count': raw.get('retweet_count'),
            'user_followers_count': raw.get('followers_count'),
            'user_friends_count': raw.get('friends_count'),
        }
        for key in counts:
            if counts[key] is not None and counts[key] < 0:
                counts[key] = None

        return cls(
                # Basic tweet info
                tweet_id=raw['id_str'],
                text=retweet['text'],
                truncated=raw['truncated'],
                lang=raw.get('lang'),

                # Basic user info
                user_id=user['id'],
                user_screen_name=user['screen_name'],
                user_name=user['name'],
                user_verified=user['verified'],
                user_location=user.get('location'),

                # Timing parameters
                created_at=parse_datetime(raw['created_at']),
                user_utc_offset=user.get('utc_offset'),
                user_time_zone=user.get('time_zone'),

                # none, low, or medium
                filter_level=raw.get('filter_level'),

                # Place
                place_name=places[0],
                place_full_name=places[1],
                place_type=places[2],
                place_country=places[3],

                # Entities
                media_url=entities.get("media"),
                urls=entities.get("urls"),
                hashtags=entities.get("hashtags"),

                # Engagement - not likely to be very useful for streamed tweets but whatever
                favorite_count=counts.get('favorite_count'),
                retweet_count=counts.get('retweet_count'),
                user_followers_count=counts.get('user_followers_count'),
                user_friends_count=counts.get('user_friends_count'),

                # Relation to other tweets
                in_reply_to_status_id=raw.get('in_reply_to_status_id'),
                retweeted_status_id=retweeted_status['id']
        )
