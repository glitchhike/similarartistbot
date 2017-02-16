import config
import pylast
import urllib2
from random import randint

def check_artist(artist):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)

    try:
        n = lastfm.get_artist(artist)
        return True
    except pylast.WSError:
        return False

def check_album(artist, album):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)

    try:
        n = lastfm.get_album(artist, album)
        return True
    except pylast.WSError:
        return False

def find_artist_image(artist):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)
    
    return lastfm.get_artist(artist).get_cover_image(2)

def find_artist(artist):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)

    # get list of at most max_to_add similar artist from last.fm
    try:
        new_similar = lastfm.get_artist(artist).get_similar(limit=config.max_to_add)
        # find all artists that meet min_score
        new_similar = [a[0].name for a in new_similar if a[1] >= config.min_score]
        # randomize choice
        r = randint(0,len(new_similar)-1)
        
        return new_similar[r]
    
    except pylast.WSError:
        return "artist not found"

def similar_artist(artist):
    a = find_artist(artist)
    resp = [a]
    if "artist not found" not in a:
        i = find_artist_image(a)
        resp.append(i)
    
    return resp

def find_album(text):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)
    
    # split text in artist - album
    s = text.split(' - ', 2)
    
    rand_similar = find_artist(s[0])
    albums = lastfm.get_artist(rand_similar).get_top_albums(limit=15)
    a = albums[randint(0,len(albums)-1)][0]
    i = a.get_cover_image()
    title = a.artist.get_name(True) + ' - ' + a.title
    print title
    print i
    print '\n'
    return [title, i]
