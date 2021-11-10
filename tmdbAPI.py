#!/usr/lib/python3
import requests
import sanction
from difflib import SequenceMatcher
from classes.TV import TV

class TMDB:

    def __init__(self, apikey='727372916fdc7ce7047ac09f25dba479'):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US'
        }

        self.config = {}

        self.config['apikey'] = apikey

        self.session = requests.Session()

        self.TV = TV(self.apikey, self.session, self.headers)
    
