import config
import pylast

def find(artist):
    # last.fm connection
    lastfm = pylast.LastFMNetwork(api_key=config.api_key, api_secret=config.api_secret)

    # get list of at most max_to_add similar artist from last.fm
    print "artist:"+artist
    new_similar = lastfm.get_artist(artist).get_similar(limit=config.max_to_add)

    # find all artists that meet min_score
    new_similar = [a[0].name for a in new_similar if a[1] >= config.min_score]

    return new_similar
