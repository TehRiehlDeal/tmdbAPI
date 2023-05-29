import requests
import sanction
from difflib import SequenceMatcher

#Exceptions
class Error(Exception):
    pass

class InvalidCredentials(Error):
    pass

class ShowNotFound(Error):
    pass

class NoSuchEpisode(Error):
    pass

class InvalidShowID(Error):
    pass

class InvalidInput(Error):
    pass

class NoActorsFound(Error):
    pass
class NoImagesFound(Error):
    pass

class TMDB:

    def __init__(self, apikey='eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MjczNzI5MTZmZGM3Y2U3MDQ3YWMwOWYyNWRiYTQ3OSIsInN1YiI6IjYwNDg0N2RiNTQ1MDhkMDA3NzU4MzJhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YL-Dvu1RPqtnYkwReU5NdtQ-0umRvVkL0GC1zy_1k30'):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            "Authorization": "Bearer {apikey}".format(apikey=apikey)
        }

        self.config = {}

        self.config['apikey'] = apikey

        self.config['apiURL'] = "https://api.themoviedb.org/3"

        self.config['tvSearchEndpoint'] = "{baseURL}/search/tv?language=en-US&query={showTitle}"

        self.config['episodeEndpoint'] = "{baseURL}/tv/{tv_id}/season/{season_number}/episode/{episode_number}?language=en-US"

        self.session = requests.Session()

    def getShow(self, name):
        if type(name) is not str:
            raise InvalidInput("You have entered an invalid name. Please try again.")
        url = self.config['tvSearchEndpoint'].format(baseURL=self.config['apiURL'], apikey=self.config['apikey'], showTitle=name)
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('total_results') == 0
        if error:
            raise ShowNotFound("Show was not found, please try again")
        return r

    def getEpisodeName(self, name, seasonNum, epNum, accuracy = 0.8, id = None):
        if type(name) is not str or type(seasonNum) is not int or type(epNum) is not int or seasonNum < 0 or epNum < 1:
            raise InvalidInput(
                "You have entered an invalid name. Please try again.")
        if (id == None):
            id = self._getShowID(name,accuracy)
        else:
            return self._getEpisodeName(id, seasonNum, epNum)
        if id == -1:
            raise InvalidShowID
        return self._getEpisodeName(id, seasonNum, epNum)


    def _getShowID(self, name, accuracy=0.8):
        url = self.config['tvSearchEndpoint'].format(baseURL=self.config['apiURL'], apikey=self.config['apikey'], showTitle=name)
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error:
            raise ShowNotFound
        for show in r['results']:
            if SequenceMatcher(None, name.lower(), show['name'].lower()).ratio() >= accuracy:
                return show['id']
        return -1

    def _getEpisodeName(self, id, seasonNum, epNum):
        url = self.config['episodeEndpoint'].format(baseURL=self.config['apiURL'], tv_id=id, season_number=seasonNum, episode_number=epNum, apikey=self.config['apikey'])
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error:
            raise NoSuchEpisode("No episode could be found. Please check season or episode number and try again.")
        return self._cleanName(r["name"])

    def _cleanName(self, name):
        newName = name.replace('\\', "").replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace("\t","")
        return newName 
    