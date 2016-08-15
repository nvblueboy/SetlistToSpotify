##Get the configuration files.

import configparser, os


class Configuration():
    def __init__(self, filename = "./config.ini"):
        #Check if the file exists.
        if os.path.isfile(filename):
            #If so, parse it.
            config = configparser.ConfigParser()
            config.read(filename)
            self.email = config["musicbrainz"]["email"]
            self.setlistKey = config["setlist.fm"]["key"]
            
            
            
        
