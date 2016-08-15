## Use the Musicbrainz XML Service to get the MBID by the artist's name.
## If the artist is not in Musicbrainz, they cannot be on setlist.fm.

import json, requests, configuration

def getid(name):
    ##Read the configuration file and get the email of the user.
    config = configuration.Configuration()
        
    ##User agent for musicbrainz and URL for request.
    headers = { "User-Agent": "SetlistToSpotify/v0.1 ( " + config.email + " )" }
    url = "http://musicbrainz.org/ws/2/artist/?query=artist:"+name+"&fmt=json"
    ## Run the request and get the text.
    r = requests.get(url,headers=headers)
    text = r.text
    ##parse the JSON into a dictionary, get the top artist's id and name.
    json_file = json.loads(text)
    artist_id = json_file["artists"][0]["id"]
    artist_name = json_file["artists"][0]["name"]
    return { 'name':artist_name, 'id':artist_id }
