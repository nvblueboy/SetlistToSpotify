## Get every song a band has performed from their setlists using the MBID.

##Standard python imports.
import json, math, requests

##Importing local modules.
import configuration, musicbrainz

def getSetlist(name,mbid_dict = None):
    ##Load the config and get the MBID of the artist.
    config = configuration.Configuration()
    if mbid_dict == None:
        mbid_dict = musicbrainz.getid(name)
    ##In case musicbrainz exceeds rate limit, alert the user.
    if mbid_dict != False:
        
        ##Make sure the artist name is right and set the URL.
        print(mbid_dict["name"])
        url = "http://api.setlist.fm/rest/0.1/artist/"+mbid_dict["id"]+"/setlists.json"

        songList = []

        ##Find out how many pages are needed.    
        ##Make the request.
        r = requests.get(url)
        text = r.text
    
        ##Parse the file.
        json_file = json.loads(text)

        total = int(json_file["setlists"]["@total"])
        perpage = int(json_file["setlists"]["@itemsPerPage"])
        pages = int(math.ceil(total/perpage))
        ##print ("Total pages: "+str(pages))
        for i in range(1,pages+1):
            ##print ("On page "+str(i))
            ##Make the request.
            r = requests.get(url+"?p="+str(i))
            text = r.text
        
            ##Parse the file.
            json_file = json.loads(text)

            ## Iterate through the JSON.

            ##Each set has it's own "setlist"
            for setlist in json_file["setlists"]["setlist"]:
                ##If there's no song data, "sets" becomes a blank string.
                if setlist["sets"] != "":
                    ## Loop through the sets in the setlist.
                    for _sets in setlist["sets"]["set"]:
                        if (len(_sets) == 0):
                            continue
                        if (len(_sets) == 1):
                            ## Find each song in each set.
                            for song in _sets["song"]:
                                ##Make sure it's a dictionary and add it to the list.
                                if type(song) == dict:
                                    songList.append(song["@name"])
        return {i for i in songList}
    else:
        print ("There was an issue getting the MBID.")
        return False

