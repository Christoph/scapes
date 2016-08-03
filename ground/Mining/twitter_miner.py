# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            # returning False in on_data disconnects the stream
            return False


class Twitter:

    def __init__(self, c_key, c_secret, a_token, a_secret):
        self.c_key = c_key
        self.c_secret = c_secret
        self.a_token = a_token
        self.a_secret = a_secret


    def connect_twitter(self):
        auth = OAuthHandler(self.c_key, self.c_secret)
        auth.set_access_token(self.a_token, self.a_secret)
        self.api = tweepy.API(auth)
        print("connected")


    def connect_to_stream(self):
        listener = StdOutListener()
        stream = Stream(self.api.auth, listener)

        stream.filter(track=['python', 'javascript', 'ruby'])



