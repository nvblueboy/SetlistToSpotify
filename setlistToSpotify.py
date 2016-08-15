##Log into spotify, create the playlist and add every song to it.

import time, json

import spotipy
import spotipy.util as util

import configuration, setlist

##Load the config.
config = configuration.Configuration()

##Scope tells the spotify user what information the app will access.
scope = "playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private"

##This will bring the user through spotify's entire login process and get a token.
token = util.prompt_for_user_token(config.user, scope,
                                   config.clientid, config.clientsecret,config.redirect)

if token:
    ##Open a spotify object.
    spotify = spotipy.Spotify(auth=token)

    ##Get the band name from the user.    
    band_name = str(input("What artist would you like to get the setlist of? "))

    ##Because musicbrainz doesn't allow calls sometimes, try 5 times before giving up.
    print("Getting setlists...")
    setlistSongs = setlist.getSetlist(band_name)
    attempt_count = 0
    while (setlistSongs == False):
        attempt_count += 1
        setlistSongs = setlist.getSetlist(band_name)
        time.sleep(1)
        if attempt_count == 5:
            break;

    ##If the setlist works,start finding spotify tracks.
    if setlistSongs != False:
        trackURIs = []
        for song in setlistSongs:
            ## look for "artist title" on spotify.
            query = band_name + " " + song
            results = spotify.search(query, type="track")
            tracks = results["tracks"]
            if len(tracks["items"])>0:
                ## The first track is usually the closest to the query, use it.
                topTrack = tracks["items"][0]["uri"]
                trackURIs.append(topTrack)
                print("Found "+query+": "+topTrack)
        ##Create the spotify playlist and get the URI.
        data = spotify.user_playlist_create(config.user, "Every Song " + band_name +" Has Played Live", False)
        uri = data["uri"]
        ##Spotify does not allow adding of more than 100 songs at a time, so add each separately.
        for i in trackURIs:
            spotify.user_playlist_add_tracks(config.user, uri, [i])
    else:
        print ("Musicbrainz seems to be having issues. Try again later.")
          
else:
    print ("Can't get token for", config.user)
