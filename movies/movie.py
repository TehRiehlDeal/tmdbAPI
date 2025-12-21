# python movie.py
"""
A lightweight client for a movie‑related REST API.

The :class:`Movie` class provides a shared HTTP session, basic
configuration (base URL, timeout, headers) and a placeholder for
endpoint‑specific methods.  Each endpoint method should follow the
pattern shown in the comments – use the private ``_request`` helper
to make the HTTP call, handle status codes, and return a typed
model or ``None`` where appropriate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Session, Response
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

# --------------------------------------------------------------------------- #
# Dataclasses describing the movie details response
# --------------------------------------------------------------------------- #

@dataclass
class Genre:
    id: int = 0
    name: str = ""

@dataclass
class ProductionCompany:
    id: int = 0
    logo_path: Optional[str] = None
    name: str = ""
    origin_country: Optional[str] = None

@dataclass
class ProductionCountry:
    iso_3166_1: Optional[str] = None
    name: Optional[str] = None

@dataclass
class SpokenLanguage:
    english_name: Optional[str] = None
    iso_639_1: Optional[str] = None
    name: Optional[str] = None

@dataclass
class MovieDetails:
    adult: bool = True
    backdrop_path: Optional[str] = None
    belongs_to_collection: Optional[str] = None
    budget: int = 0
    genres: List[Genre] = None
    homepage: Optional[str] = None
    id: int = 0
    imdb_id: Optional[str] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: float = 0.0
    poster_path: Optional[str] = None
    production_companies: List[ProductionCompany] = None
    production_countries: List[ProductionCountry] = None
    release_date: Optional[str] = None
    revenue: int = 0
    runtime: int = 0
    spoken_languages: List[SpokenLanguage] = None
    status: Optional[str] = None
    tagline: Optional[str] = None
    title: Optional[str] = None
    video: bool = True
    vote_average: float = 0.0
    vote_count: int = 0

@dataclass
class Rated:
    """The rating the user has given to the movie."""
    value: int = 0


@dataclass
class AccountState:
    """Response schema for `/movie/{movie_id}/account_states`."""
    id: int = 0
    favorite: bool = True
    rated: Rated = None
    watchlist: bool = True

@dataclass
class AlternativeTitle:
    """Single alternative title returned by the API."""
    iso_3166_1: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None


@dataclass
class AlternativeTitles:
    """Response schema for `/movie/{movie_id}/alternative_titles`."""
    id: int = 0
    titles: List[AlternativeTitle] = None



class MovieError(Exception):
    """Base exception for all errors raised by the Movie client."""


class MovieNotFoundError(MovieError):
    """Raised when a requested resource is not found (HTTP 404)."""


class MovieAuthenticationError(MovieError):
    """Raised when authentication fails (HTTP 401/403)."""


class MovieServerError(MovieError):
    """Raised for server‑side errors (HTTP 5xx)."""


@dataclass
class Movie:
    """
    Client for the movie API.

    Args:
        base_url: Base URL of the API (e.g. ``https://api.example.com``).
        timeout: Request timeout in seconds.
        api_key: Optional API key to be added to the ``Authorization`` header.
    """

    base_url: str
    timeout: float = 10.0
    api_key: Optional[str] = None

    def __post_init__(self) -> None:
        self._session: Session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        if self.api_key:
            self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Internal helper to perform an HTTP request and raise typed errors.

        Args:
            method: HTTP method ('GET', 'POST', etc.).
            endpoint: API path relative to ``base_url``.
            params: Query parameters.
            data: Request payload (will be JSON‑encoded).

        Returns:
            Decoded JSON response as ``dict`` or ``list``.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response: Response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except HTTPError as exc:
            if exc.response is not None:
                status = exc.response.status_code
                if status == 404:
                    raise MovieNotFoundError(f"Resource not found: {url}") from exc
                if status in (401, 403):
                    raise MovieAuthenticationError(f"Authentication failed: {url}") from exc
                if 500 <= status < 600:
                    raise MovieServerError(f"Server error ({status}): {url}") from exc
            raise MovieError(f"HTTP error for {url}") from exc
        except Timeout as exc:
            raise MovieError(f"Request timed out for {url}") from exc
        except ConnectionError as exc:
            raise MovieError(f"Connection error for {url}") from exc
        except RequestException as exc:
            raise MovieError(f"Request exception for {url}") from exc

        if response.content:
            return response.json()
        return None

    def get_movie_details(
        self,
        movie_id: int,
        *,
        append_to_response: Optional[str] = None,
        language: str = "en-US",
    ) -> MovieDetails:
        """
        Retrieve detailed information for a specific movie.

        Args:
            movie_id: The unique identifier of the movie (int32).
            append_to_response: Comma‑separated list of endpoints to include in the response
                (max 20 items).
            language: Language code for the returned text (defaults to ``en-US``).

        Returns:
            A :class:`MovieDetails` instance populated with the API response.

        Raises:
            MovieNotFoundError: If the movie does not exist.
            MovieAuthenticationError: If authentication fails.
            MovieServerError: If the server returns a 5xx error.
        """
        params: Dict[str, str] = {"language": language}
        if append_to_response:
            params["append_to_response"] = append_to_response

        endpoint = f"movie/{movie_id}"
        raw_data = self._request("GET", endpoint, params=params)

        # Convert the raw dict into typed dataclasses
        def _parse_list(cls, items):
            return [cls(**item) for item in items] if items else []

        movie = MovieDetails(
            adult=raw_data.get("adult", True),
            backdrop_path=raw_data.get("backdrop_path"),
            belongs_to_collection=raw_data.get("belongs_to_collection"),
            budget=raw_data.get("budget", 0),
            genres=_parse_list(Genre, raw_data.get("genres")),
            homepage=raw_data.get("homepage"),
            id=raw_data.get("id", 0),
            imdb_id=raw_data.get("imdb_id"),
            original_language=raw_data.get("original_language"),
            original_title=raw_data.get("original_title"),
            overview=raw_data.get("overview"),
            popularity=raw_data.get("popularity", 0.0),
            poster_path=raw_data.get("poster_path"),
            production_companies=_parse_list(ProductionCompany, raw_data.get("production_companies")),
            production_countries=_parse_list(ProductionCountry, raw_data.get("production_countries")),
            release_date=raw_data.get("release_date"),
            revenue=raw_data.get("revenue", 0),
            runtime=raw_data.get("runtime", 0),
            spoken_languages=_parse_list(SpokenLanguage, raw_data.get("spoken_languages")),
            status=raw_data.get("status"),
            tagline=raw_data.get("tagline"),
            title=raw_data.get("title"),
            video=raw_data.get("video", True),
            vote_average=raw_data.get("vote_average", 0.0),
            vote_count=raw_data.get("vote_count", 0),
        )
        return movie
    
    def get_account_state(
        self,
        movie_id: int,
        *,
        session_id: Optional[str] = None,
        guest_session_id: Optional[str] = None,
    ) -> AccountState:
        """
        Retrieve account states for a specific movie.

        Args:
            movie_id: The unique identifier of the movie (int32).
            session_id: User session ID (for logged‑in users).
            guest_session_id: Guest session ID (for non‑logged‑in users).

        Returns:
            An :class:`AccountState` instance populated with the API response.

        Raises:
            MovieNotFoundError: If the movie does not exist.
            MovieAuthenticationError: If authentication fails.
            MovieServerError: If the server returns a 5xx error.
        """
        params: Dict[str, str] = {}
        if session_id:
            params["session_id"] = session_id
        if guest_session_id:
            params["guest_session_id"] = guest_session_id

        endpoint = f"movie/{movie_id}/account_states"
        raw_data = self._request("GET", endpoint, params=params)

        # Convert raw dict to typed dataclasses
        rated_obj = Rated(**raw_data.get("rated", {})) if raw_data.get("rated") else Rated()
        return AccountState(
            id=raw_data.get("id", 0),
            favorite=raw_data.get("favorite", True),
            rated=rated_obj,
            watchlist=raw_data.get("watchlist", True),
        )
    
    def get_alternative_titles(
        self,
        movie_id: int,
        *,
        country: Optional[str] = None,
    ) -> AlternativeTitles:
        """
        Retrieve alternative titles for a specific movie.

        Args:
            movie_id: The unique identifier of the movie (int32).
            country: ISO‑3166‑1 code to filter titles by country.

        Returns:
            An :class:`AlternativeTitles` instance containing the list
            of titles returned by the API.

        Raises:
            MovieNotFoundError: If the movie does not exist.
            MovieAuthenticationError: If authentication fails.
            MovieServerError: If the server returns a 5xx error.
        """
        params: Dict[str, str] = {}
        if country:
            params["country"] = country

        endpoint = f"movie/{movie_id}/alternative_titles"
        raw_data = self._request("GET", endpoint, params=params)

        titles = [
            AlternativeTitle(**t) for t in raw_data.get("titles", [])
        ] or []

        return AlternativeTitles(
            id=raw_data.get("id", 0),
            titles=titles,
        )