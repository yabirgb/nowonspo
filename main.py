# -*- coding: utf-8 -*-

#to use timer uncomment arrow import and timers marks

from twython import Twython
import json
import urllib2
#import arrow

#momento = arrow.now('local') #just a way to test speed

#app settings
app_key = ''
app_secret = ''
access_token = '' 
access_token_secret = '' 

twitter = Twython(app_key, app_secret, access_token, access_token_secret)
#tweets = twitter.search(q='#nowplaying spotify')

#define the tweets search
search = twitter.search

#function to get urls from a redirect
def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

#get the track from "open" urls
def track_number(url):
    return url.split("/")[4]

#get the tacks from tweets
def get_urls(magic_url):
	#different kinds of possible urls
    if "spoti.fi" in magic_url:
        true_url =  get_redirected_url(magic_url)
        tracked = track_number(true_url)

        if len(tracked) == 22:
            track = tracked

    elif "open.spotify.com" in magic_url:
        tracked = track_number(magic_url)
        if len(tracked) == 22:
            track = tracked
    else:
        error =  "Not a valid url"

    #print track
    return track

#main loop to get 3 pages of urls
for i in xrange(3):
    if i == 0:
        tweets = search(q='#nowplaying spotify')

        for tweet in tweets['statuses']:
            magic_url = tweet['entities']['urls'][0]['expanded_url'].encode('utf-8')

            try:
                print "http://open.spotify.com/track/" + get_urls(magic_url)

            except:
                error = "Probably more than 1 url"

        id_number = tweets['statuses'][-1]['id']

    else:
        tweets = search(q='#nowplaying spotify', max_id = id_number)
        for tweet in tweets['statuses']:

            magic_url = tweet['entities']['urls'][0]['expanded_url'].encode('utf-8')

            try:
                print "http://open.spotify.com/track/" + get_urls(magic_url)
            except:
                error = "Probably more than 1 url"

        id_number = tweets['statuses'][-1]['id']

#new_momento = arrow.now('local')#check again the time

#print new_momento - momento #return diference
