import requests
import sanction
from difflib import SequenceMatcher
from Errors import Exception, InvalidCredentials, ShowNotFound, NoSuchEpisode, InvalidShowID, InvalidInput, NoActorsFound, NoImagesFound


class TV:
    def __init__(self, apiKey, session, headers):
        self.apiKey = apiKey

        self.headers = headers

        self.config['apiURL'] = "https://api.themoviedb.org/3"

        self.config['tvSearchEndpoint'] = "{baseURL}/search/tv?api_key={apikey}&language=en-US&query={showTitle}"

        self.config['tvDetailEndpoint'] = "{baseURL}/tv/{tv_id}"

        self.config['episodeEndpoint'] = "{baseURL}/tv/{tv_id}/season/{season_number}/episode/{episode_number}?language=en-US&api_key={apikey}"

        self.session = session

    def searchShow(self, name):
        if type(name) is not str:
            raise InvalidInput(
                "You have entered an invalid name. Please try again.")
        url = self.config['tvSearchEndpoint'].format(
            baseURL=self.config['apiURL'], apikey=self.config['apikey'], showTitle=name)
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error:
            raise ShowNotFound("Show was not found, please try again")
        return r

    def getShowDetails(self, id):
        if type(id) is not int or id < 0:
            raise InvalidInput("You have entered an invalid id. Please try again.")
        url = self.config['tvDetailEndpoint'].format(baseURL=self.config['apiURL'], apikey=self.apiKey, tv_id=id)
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error: 
            raise ShowNotFound("Show was not found, please try again.")
        return r


    def getEpisodeName(self, name, seasonNum, epNum, accuracy=0.8, id=None):
        if type(name) is not str or type(seasonNum) is not int or type(epNum) is not int or seasonNum < 0 or epNum < 1:
            raise InvalidInput(
                "You have entered an invalid name. Please try again.")
        if (id == None):
            id = self._getShowID(name, accuracy)
        else:
            return self._getEpisodeName(id, seasonNum, epNum)
        if id == -1:
            raise InvalidShowID
        return self._getEpisodeName(id, seasonNum, epNum)

    def _getShowID(self, name, accuracy=0.8):
        url = self.config['tvSearchEndpoint'].format(
            baseURL=self.config['apiURL'], apikey=self.config['apikey'], showTitle=name)
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error:
            raise ShowNotFound
        for show in r['results']:
            if SequenceMatcher(None, name.lower(), show['name'].lower()).ratio() >= accuracy:
                return show['id']
        return -1

    def _getEpisodeName(self, id, seasonNum, epNum):
        url = self.config['episodeEndpoint'].format(
            baseURL=self.config['apiURL'], tv_id=id, season_number=seasonNum, episode_number=epNum, apikey=self.config['apikey'])
        r = self.session.get(url, headers=self.headers).json()
        error = r.get('Error')
        if error:
            raise NoSuchEpisode(
                "No episode could be found. Please check season or episode number and try again.")
        return self._cleanName(r["name"])

    def _cleanName(self, name):
        newName = name.replace('\\', "").replace("/", "").replace(":", "").replace("*", "").replace(
            "?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace("\t", "")
        return newName
