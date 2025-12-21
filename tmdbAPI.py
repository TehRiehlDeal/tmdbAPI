from typing import Optional
import requests
import sanction
from classes.search import Search
from difflib import SequenceMatcher
from movies.movie import Movie
from settings import settings

# Exceptions


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

    def __init__(self, *, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.api_key
        self.base_url = settings.base_url
        self.timeout = settings.timeout
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            f"Authorization": f"Bearer {self.api_key}"
        }

        self.config = {}

        self.config['apikey'] = self.api_key

        self.config['apiURL'] = "https://api.themoviedb.org/3"

        self.config['episodeEndpoint'] = "{baseURL}/tv/{tv_id}/season/{season_number}/episode/{episode_number}?language=en-US"

        self.session = requests.Session()

        self.search = Search(apikey=self.api_key, session=self.session)

        self.movie = Movie(
            base_url=self.base_url,
            timeout=self.timeout,
            api_key=self.api_key,
            session=self.session
        )

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
        r = self.search.searchTV(name)
        error = r.get('Error')
        if error:
            raise ShowNotFound
        for show in r['results']:
            if SequenceMatcher(None, name.lower(), show['name'].lower()).ratio() >= accuracy:
                return show['id']
        return -1

    def _getEpisodeName(self, id, seasonNum, epNum):
        url = self.config['episodeEndpoint'].format(
            baseURL=self.config['apiURL'], tv_id=id, season_number=seasonNum, episode_number=epNum)
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
