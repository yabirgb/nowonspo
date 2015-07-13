# -*- coding: utf-8 -*-

from twython import Twython
import urllib2

from datetime import datetime

tstart = datetime.now()



#app settings, fill with your app credentials
app_key = ''
app_secret = ''
access_token = '' 
access_token_secret = '' 

twitter = Twython(app_key, app_secret, access_token, access_token_secret)

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
lista_usuarios = []

while contador == 0 or contador < 30:
    if id_number != 0:
        tweets = search(q='#nowplaying spotify', max_id= id_number) #make the search looking for older tweets
    else:
        tweets = search(q='#nowplaying spotify')#initial search

    for tweet in tweets['statuses']:
        #by using this filter we prevent from getting albums but it can fail
        if "by" or "de" in tweet["statuses"]["text"].split(" "): 
            magic_url = tweet['entities']['urls'][0]['expanded_url'].encode('utf-8')#the tweet url
            if str(tweet['user']['screen_name']) not in lista_usuarios:
                lista_usuarios.append(str(tweet['user']['screen_name']))	
                print "http://open.spotify.com/track/" + get_urls(magic_url) #get the spotify url
                print str(tweet["text"].encode('utf-8'))+ "\n"

                contador += 1

    id_number = tweets['statuses'][-1]['id'] # return the las id

tfinish = datetime.now()

result = tfinish - tstart
result = result.seconds

print "Printed " + str(contador) + " tracks in " + str(result) + "seconds"
