import tweepy
from pymongo import MongoClient

# Authenticate to Twitter
auth = tweepy.OAuthHandler("GuM7AWR472RNPoQHbTEQArbyw", "U9jhBsBryqiCW99ujUYEJKB4OtXPYB74T2V7nhsSRuiYBLctJB")
auth.set_access_token("465827087-dKE0ELcXKd8TAJ03IJb7FoC6WXFt1pnmXALpGG5n", "oUx8SG9klZZU7o72ycZ4ai8DBCIKL0L4JpEzBVaAKkvjG")


# MongoDB Database connection setup
client = MongoClient("mongodb://localhost:27017/")
db  = client.twitter_crawler
collection = db.smalldb

# Create API object
api = tweepy.API(auth)


# REST API calls
rest = api.search(['president', 'trump', 'whitehouse'], lang=["en"])


for item in rest:
    collection.insert_one(item._json)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        collection.insert_one(status._json)



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['president', 'trump', 'whitehouse'], languages=["en"])

