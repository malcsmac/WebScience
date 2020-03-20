import tweepy
from pymongo import MongoClient

# Authenticate to Twitter
auth = tweepy.OAuthHandler("GuM7AWR472RNPoQHbTEQArbyw", "U9jhBsBryqiCW99ujUYEJKB4OtXPYB74T2V7nhsSRuiYBLctJB")
auth.set_access_token("465827087-dKE0ELcXKd8TAJ03IJb7FoC6WXFt1pnmXALpGG5n", "oUx8SG9klZZU7o72ycZ4ai8DBCIKL0L4JpEzBVaAKkvjG")


# MongoDB Database connection setup
client = MongoClient("mongodb://localhost:27017/")
db  = client.twitter_crawler
collection = db['tweets']

# Create API object
api = tweepy.API(auth)


# REST API calls
rest = api.search(['president', 'trump', 'whitehouse'], lang=["en"])


for item in rest:
##    username = rest[item]._json["user"]["screen_name"]
##    text = rest[item]._json["text"]
##    date = rest[item]._json["created_at"]
##
##    #parse date
##    created = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
##    print(created)
##
##    tweetDoc = { "date": created, "username": username, "text": text }
    db.tweets.insert_one(item._json)




# Create a tweet

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        db.tweets.insert_one(status._json)
##        print(status)



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['president', 'trump', 'whitehouse'], languages=["en"])

