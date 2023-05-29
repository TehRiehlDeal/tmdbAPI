# Exceptions


class Error(Exception):
    pass


class InvalidCredentials(Error):
    pass


class CollectionNotFound(Error):
    pass


class CompanyNotFound(Error):
    pass


class KeywordNotFound(Error):
    pass


class MovieNotFound(Error):
    pass


class MultiNotFound(Error):
    pass


class PersonNotFound(Error):
    pass


class TVNotFound(Error):
    pass


class InvalidInput(Error):
    pass


class Search:
    def __init__(self, apikey, session):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US',
            "Authorization": "Bearer {apikey}".format(apikey=apikey)
        }

        self.config = {}

        self.config['apiURL'] = "https://api.themoviedb.org/3"

        self.config['searchEndpoint'] = "{baseURL}/search/{scope}"

        self.session = session

    def searchCollection(self, query, includeAdult=False, language="en-US", page=1, region=""):
        if type(query) is not str or type(includeAdult) is not bool or type(language) is not str or type(page) is not int or type(region) is not str:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="collection")
        params = {
            'query': query,
            'include_adult': includeAdult,
            'language': language,
            'page': page,
            'region': region
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise CollectionNotFound(
                "Collection was not found, please try again")
        return r

    def searchCompany(self, query, page=1):
        if type(query) is not str or type(page) is not int:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="company")
        params = {
            'query': query,
            'page': page,
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise CompanyNotFound("Company was not found, please try again")
        return r

    def searchKeyword(self, query, page=1):
        if type(query) is not str or type(page) is not int:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="keyword")
        params = {
            'query': query,
            'page': page,
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise KeywordNotFound("Keyword was not found, please try again")
        return r

    def searchMovie(self, query, includeAdult=False, language="en-US", primaryReleaseYear="", page=1, region="", year=""):
        if type(query) is not str or type(includeAdult) is not bool or type(language) is not str or type(primaryReleaseYear) is not str or type(page) is not int or type(region) is not str or type(year) is not str:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="movie")
        params = {
            'query': query,
            'include_adult': includeAdult,
            'language': language,
            'primary_release_year': primaryReleaseYear,
            'page': page,
            'region': region,
            'year': year
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise MovieNotFound("Movie was not found, please try again")
        return r

    def searchMulti(self, query, includeAdult=False, language="en-US", page=1):
        if type(query) is not str or type(includeAdult) is not bool or type(language) is not str or type(page) is not int:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="multi")
        params = {
            'query': query,
            'include_adult': includeAdult,
            'language': language,
            'page': page,
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise MultiNotFound(
                "Movie or TV show was not found, please try again")
        return r

    def searchPerson(self, query, includeAdult=False, language="en-US", page=1):
        if type(query) is not str or type(includeAdult) is not bool or type(language) is not str or type(page) is not int:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="person")
        params = {
            'query': query,
            'include_adult': includeAdult,
            'language': language,
            'page': page,
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise PersonNotFound(
                "Person was not found, please try again")
        return r

    def searchTV(self, query, firstAirDateYear="", includeAdult=False, language="en-US", page=1, year=""):
        if type(query) is not str or type(firstAirDateYear) is not str or type(includeAdult) is not bool or type(language) is not str or type(page) is not int or type(year) is not str:
            raise InvalidInput(
                "You have made an invalid search. Please try again.")
        url = self.config['searchEndpoint'].format(
            baseURL=self.config['apiURL'], scope="tv")
        params = {
            'query': query,
            'first_air_date_year': firstAirDateYear,
            'include_adult': includeAdult,
            'language': language,
            'page': page,
            'year': year
        }
        r = self.session.get(url, headers=self.headers, params=params).json()
        error = r.get('total_results') == 0
        if error:
            raise TVNotFound("TV show was not found, please try again")
        return r
