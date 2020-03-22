import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import adjusted_rand_score
import re
from collections import Counter

client = pymongo.MongoClient('localhost', 27017)
db = client.twitter_crawler
tweets = db.smalldb

documents = []
text = []
username_data = []
hashtag_data = []


if __name__ == "__main__":
    print("=== Retrieving tweets from database ===")
    for tweet in tweets.find():
        try:
            text.append(tweet['text'])
            if tweet['truncated'] == True:
                documents.append({tweet['user']['screen_name'] : tweet['extended_tweet']['full_text']})
            else:
                documents.append({tweet['user']['screen_name'] :  tweet['text']})
        except:
            pass
## cluster users and hashtags
    print("=== Vectorising ===")
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(documents)

    true_k = 10
    print("=== Preforming KMeans with %d clusters ===" % true_k)
    model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
    model.fit(X)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        # Set up blank list for group usernames and hashtags
        hashtag_data.append([])
        username_data.append([])
        print("Cluster %d, Size: %d" % (i,len(order_centroids[i])/10))
        for ind in order_centroids[i, :10]:
            # After clustering data is returned as a string
            tweet_string = terms[ind]
            # Add '@' for regex later on to collected username of tweeter
            tweet_string = "@" + tweet_string
            usernames = re.findall(r'(@\w+)', tweet_string)
            hashtags = re.findall(r'(#\w+)', terms[ind])
            for username in usernames:
                username_data[i].append(username)
            for hashtag in hashtags:
                hashtag_data[i].append(hashtag)

        print("Usernames:")
        print(Counter(username_data[i]).most_common(5))
        if not hashtag_data[i] == []:
            print("Hashtags:")
            print(Counter(hashtag_data[i]).most_common(5))
        else:
            print("Hashtags:")


## cluster text
    vectorizer = TfidfVectorizer(analyzer='word', stop_words="english")
    X = vectorizer.fit_transform(text)

    true_k = 10
    model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d, Size: %d" % (i,len(order_centroids[i])/10))
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind])
    
   