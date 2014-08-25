# -*- coding: utf-8 -*-

#to use timer uncomment arrow import and timer marks

from twython import Twython
import urllib2
#import arrow

#momento = arrow.now('local') #just a way to test speed

#app settings, fill with your app credentials
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

id_number = 0 #id for searchs in twitter
contador = 0 #used in the while to count tracks

#Is possible to get many bad urls or tweets where this code is not able to catch urls
#so this while does that at least you get 30 songs but for example you get 29 the while
#will get the next 15 tweets and extract the urls so you watchng to 44 
while contador == 0 or contador <= 30:
    if id_number != 0:
        tweets = search(q='#nowplaying spotify', max_id= id_number) #make the search looking for older tweets
    else:
        tweets = search(q='#nowplaying spotify')#initial search

    for tweet in tweets['statuses']:
        magic_url = tweet['entities']['urls'][0]['expanded_url'].encode('utf-8')#the tweet url
        try:
            print "http://open.spotify.com/track/" + get_urls(magic_url)#get the spotify url
            contador += 1

        except:
            error = "Probably more than 1 url"

    id_number = tweets['statuses'][-1]['id'] # return the las id

#new_momento = arrow.now('local')#check again the time

#time = new_momento - momento
print "Printed " + str(contador) + " tracks in " #+ str(time)
