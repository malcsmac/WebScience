# Tweets Clustering using k-means

Web Science
================

Web Sciences (H) COMPSCI4077, Network based Social Media Analytics
 
Twitter Crawler.py
================
Crawls twitter for tweets containing the given keywords and stores in a mongodb.
To run: edit the mongoDB connection details (database name and collection). Change the keywords and language to whatever you desire in both the REST crawler and the streamer.

k-means-cluster.py
================
Uses k-means to group usernames and hashtags then text.
To run: edit the mongoDB connection details (database name and collection). 


Tweets.json
================
Exported json file of mongodb, import to mongodb for above python files to work