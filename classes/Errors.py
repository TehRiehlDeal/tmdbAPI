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
