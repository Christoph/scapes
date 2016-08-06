from django.db import models
from datetime import datetime
from django.utils import timezone
from email._parseaddr import parsedate

current_timezone = timezone.get_current_timezone()


def parse_datetime(string):
    return datetime(*(parsedate(string)[:6]), tzinfo=current_timezone)


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
class Tweet(models.Model):
    # Basic tweet info
    tweet_id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=250)
    truncated = models.BooleanField(default=False)
    lang = models.CharField(max_length=9, null=True, blank=True, default=None)

    # Basic user info
    user_id = models.BigIntegerField()
    user_screen_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=150)
    user_verified = models.BooleanField(default=False)

    # Timing parameters
    created_at = models.DateTimeField(db_index=True)  # should be UTC
    user_utc_offset = models.IntegerField(null=True, blank=True, default=None)
    user_time_zone = models.CharField(max_length=150, null=True, blank=True, default=None)

    # none, low, or medium
    filter_level = models.CharField(max_length=6, null=True, blank=True, default=None)

    # Geo parameters
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    user_geo_enabled = models.BooleanField(default=False)
    user_location = models.CharField(max_length=150, null=True, blank=True, default=None)

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

        user = raw['user']
        retweeted_status = raw.get('retweeted_status')
        if retweeted_status is None:
            retweeted_status = {'id': None}

        # The "coordinates" entry looks like this:
        #
        # "coordinates":
        # {
        #     "coordinates":
        #     [
        #         -75.14310264,
        #         40.05701649
        #     ],
        #     "type":"Point"
        # }

        coordinates = (None, None)
        if raw['coordinates']:
            coordinates = raw['coordinates']['coordinates']

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
                tweet_id=raw['id'],
                text=raw['text'],
                truncated=raw['truncated'],
                lang=raw.get('lang'),

                # Basic user info
                user_id=user['id'],
                user_screen_name=user['screen_name'],
                user_name=user['name'],
                user_verified=user['verified'],

                # Timing parameters
                created_at=parse_datetime(raw['created_at']),
                user_utc_offset=user.get('utc_offset'),
                user_time_zone=user.get('time_zone'),

                # none, low, or medium
                filter_level=raw.get('filter_level'),

                # Geo parameters
                latitude=coordinates[1],
                longitude=coordinates[0],
                user_geo_enabled=user.get('geo_enabled'),
                user_location=user.get('location'),

                # Engagement - not likely to be very useful for streamed tweets but whatever
                favorite_count=counts.get('favorite_count'),
                retweet_count=counts.get('retweet_count'),
                user_followers_count=counts.get('user_followers_count'),
                user_friends_count=counts.get('user_friends_count'),

                # Relation to other tweets
                in_reply_to_status_id=raw.get('in_reply_to_status_id'),
                retweeted_status_id=retweeted_status['id']
        )