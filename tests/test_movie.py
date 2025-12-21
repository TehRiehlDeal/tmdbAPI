# tests/test_movie.py
"""
Unit tests for :mod:`movies.movie`.
"""

import pytest
from unittest.mock import Mock

from requests.exceptions import HTTPError

# Import the client & dataclasses we want to exercise
from movies.movie import Movie, MovieError, MovieNotFoundError, \
    MovieAuthenticationError, MovieServerError, Genre, ProductionCompany, \
    ProductionCountry, SpokenLanguage, Rated, AccountState, AlternativeTitle, \
    AlternativeTitles


@pytest.fixture
def dummy_movie():
    """
    Return a minimal :class:`Movie` instance that does *not* hit the real API.
    The ``_request`` method is monkey‑patched by the tests.
    """
    return Movie(base_url="https://api.fake", timeout=1.0, api_key=None)


# ------------------------------------------------------------
# Helper to replace ``Movie._request`` while capturing its arguments
# ------------------------------------------------------------
def stub_request(expected_endpoint: str, response: dict = None, exception: Exception = None):
    """
    Return a stub that mimics ``Movie._request``.
    It will raise ``exception`` if supplied, otherwise return ``response``.
    """
    def _stub(method: str, endpoint: str, *, params=None, data=None):
        # Basic sanity check – the endpoint must match what we expect
        assert endpoint == expected_endpoint, f"Expected endpoint {expected_endpoint}, got {endpoint}"
        if exception is None:
            return response
        raise exception
    return _stub


# ------------------------------------------------------------
# Happy‑path tests
# ------------------------------------------------------------
def test_get_movie_details_parsing(dummy_movie):
    """
    Verify that :meth:`Movie.get_movie_details` correctly parses a
    realistic JSON payload.
    """
    payload = {
        "adult": False,
        "backdrop_path": "/path.jpg",
        "belongs_to_collection": "Some Collection",
        "budget": 150_000_000,
        "genres": [{"id": 1, "name": "Action"}],
        "homepage": "https://example.com",
        "id": 42,
        "imdb_id": "tt1234567",
        "original_language": "en",
        "original_title": "Original Title",
        "overview": "A great movie",
        "popularity": 99.9,
        "poster_path": "/poster.jpg",
        "production_companies": [
            {"id": 10, "name": "Studio", "logo_path": None, "origin_country": "US"}
        ],
        "production_countries": [{"iso_3166_1": "US", "name": "United States"}],
        "release_date": "2021-01-01",
        "revenue": 200_000_000,
        "runtime": 120,
        "spoken_languages": [{"english_name": "English", "iso_639_1": "en", "name": "English"}],
        "status": "Released",
        "tagline": "Tagline",
        "title": "Movie Title",
        "video": False,
        "vote_average": 8.5,
        "vote_count": 1500,
    }

    dummy_movie._request = stub_request("movie/42", payload)
    details = dummy_movie.get_movie_details(42, append_to_response="credits")
    assert details.id == 42
    assert details.adult is False
    assert details.backdrop_path == "/path.jpg"
    assert len(details.genres) == 1
    assert details.genres[0].name == "Action"
    assert details.production_companies[0].name == "Studio"
    assert details.production_countries[0].iso_3166_1 == "US"
    assert details.spoken_languages[0].iso_639_1 == "en"
    assert details.video is False
    assert details.vote_average == 8.5


def test_get_account_state_parsing(dummy_movie):
    """
    Verify that :meth:`Movie.get_account_state` correctly parses the
    nested ``rated`` object and falls back to defaults when missing.
    """
    payload = {
        "id": 42,
        "favorite": True,
        "rated": {"value": 7},
        "watchlist": False,
    }

    dummy_movie._request = stub_request("movie/42/account_states", payload)
    state = dummy_movie.get_account_state(42, session_id="abc123")

    assert state.id == 42
    assert state.favorite is True
    assert state.rated.value == 7
    assert state.watchlist is False


def test_get_account_state_missing_rated(dummy_movie):
    """
    When the ``rated`` field is omitted, ``Rated`` defaults to ``value=0``.
    """
    payload = {
        "id": 42,
        "favorite": False,
        "watchlist": True,
    }

    dummy_movie._request = stub_request("movie/42/account_states", payload)
    state = dummy_movie.get_account_state(42, guest_session_id="guest123")

    assert state.id == 42
    assert state.favorite is False
    assert state.rated.value == 0   # default
    assert state.watchlist is True


def test_get_alternative_titles_parsing(dummy_movie):
    """
    Verify that :meth:`Movie.get_alternative_titles` returns the list of
    :class:`AlternativeTitle` objects correctly.
    """
    payload = {
        "id": 42,
        "titles": [
            {"iso_3166_1": "US", "title": "Alt Title 1", "type": "Theatrical"},
            {"iso_3166_1": "GB", "title": "Alt Title 2", "type": "TV"},
        ],
    }

    dummy_movie._request = stub_request("movie/42/alternative_titles", payload)
    alt = dummy_movie.get_alternative_titles(42, country="US")

    assert alt.id == 42
    assert len(alt.titles) == 2
    assert alt.titles[0].iso_3166_1 == "US"
    assert alt.titles[0].title == "Alt Title 1"
    assert alt.titles[1].type == "TV"


# ------------------------------------------------------------
# Error‑handling tests
# ------------------------------------------------------------
def test_request_raises_404(dummy_movie):
    """
    Ensure that a 404 response from ``_request`` is translated to
    :class:`MovieNotFoundError`.
    """
    class DummyResp:
        status_code = 404

    def raise_404(*args, **kwargs):
        # This is the *actual* request call that _request makes.
        raise HTTPError(response=DummyResp())

    # Patch only the underlying request – leave _request untouched.
    dummy_movie._session.request = raise_404

    with pytest.raises(MovieNotFoundError):
        dummy_movie.get_movie_details(999)


def test_request_raises_auth_error(dummy_movie):
    """
    Ensure that a 401/403 response is translated to :class:`MovieAuthenticationError`.
    """
    class DummyResp:
        status_code = 401

    def raise_401(*args, **kwargs):
        raise HTTPError(response=DummyResp())

    dummy_movie._session.request = raise_401

    with pytest.raises(MovieAuthenticationError):
        dummy_movie.get_movie_details(999)


def test_request_raises_server_error(dummy_movie):
    """
    Ensure that a 5xx response is translated to :class:`MovieServerError`.
    """
    class DummyResp:
        status_code = 502

    def raise_5xx(*args, **kwargs):
        raise HTTPError(response=DummyResp())

    dummy_movie._session.request = raise_5xx

    with pytest.raises(MovieServerError):
        dummy_movie.get_movie_details(999)
