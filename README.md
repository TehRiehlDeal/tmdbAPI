# tmdbAPI – A Minimal Python Client for the TMDB API

*A lightweight, typed wrapper around The Movie Database (TMDB) API.*

---

## 📦 Installation

```bash
# Create a virtualатов environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package locally (editable mode)
pip install -e .
```

> **Why `-e`?**  
> The editable install keeps your source in sync with the running
> interpreter – any changes you make will be visible immediately.

---

## 🚀 Quick Start

```python
from tmdbAPI import TMDB

# Replace the default key with your own or pass it explicitly
tmdb = TMDB(apikey="YOUR_TMDB_BEARER_TOKEN")

# ---------- 1️⃣ Classic episode lookup ----------
name, season, episode = "Breaking Bad", 5, 14
print(tmdb.getEpisodeName(name, season, episode))
# ➜ “Felina”

# ---------- 2️⃣ TV‑show search ----------
show_id = tmdb._getShowID("Stranger Things", accuracy=0.8)
print(show_id)
# ➜ 1396

# ---------- 3️⃣ Use the new Movie helper ----------
# All public movie helpers live under `tmdb.movie`
print(tmdb.movie.get_movie_details(550))          # -> MovieDetails dataclass
print(tmdb.movie.get_alternative_titles(550))     # -> AlternativeTitles dataclass
```

> The `TMDB` class still provides the legacy TV‑episode helpers
> (`getEpisodeName`, `_getShowID`, …) **unchanged**.

---

## 📚 API Reference

### `TMDB`

| Method | Purpose | Raises |
|--------|---------|--------|
| `getEpisodeName(name, seasonNum, epNum, accuracy=0.8, id=None)` | Return the episode title (sanitised) for a given TV show. | `InvalidInput`, `ShowNotFound`, `NoSuchEpisode`, `InvalidShowID` |
| `search` (via `Search` instance) | Search TV shows by name. | `ShowNotFound` |
| **`movie`** | **New** – a fully‑typed movie helper. | – |

#### `movie` helpers

| Method | Description | Example |
|--------|-------------|---------|
| `get_movie_details(movie_id: int)` | Returns a `MovieDetails` dataclass. | `tmdb.movie.get_movie_details(550)` |
| `get_alternative_titles(movie_id: int)` | Returns an `AlternativeTitles` dataclass. | `tmdb.movie.get_alternative_titles(550)` |
| `get_account_state(movie_id: int)` | Returns an `AccountState` dataclass. | `tmdb.movie.get_account_state(550)` |
| `get_credits(movie_id: int)` | Returns a `Credits` dataclass. | `tmdb.movie.get_credits(550)` |
| `get_videos(movie_id: int)` | Returns a `Videos` dataclass. | `tmdb.movie.get_videos(550)` |
| `get_images(movie_id: int)` | Returns a `Images` dataclass. | `tmdb.movie.get_images(550)` |
| `get_wikipedia_page(movie_id: int)` | Returns a `WikipediaPage` dataclass. | `tmdb.movie.get_wikipedia_page(550)` |

> All of these helpers accept the same `apikey` and `session` you pass to
> the top‑level `TMDB` constructor.

---

## 👀 Legacy TV‑episode lookup (unchanged)

```python
tmdb = TMDB(apikey="YOUR_TOKEN")
episode_name = tmdb.getEpisodeName("Breaking Bad", 5, 14)
print(episode_name)  # ➜ “Felina”
```

---

## 🤝 Contributing

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) if you’d like to help
expand or improve this library.

---

## 📄 License

MIT © 2024 – see the [LICENSE](LICENSE) file.

> **Disclaimer** – This wrapper is a thin façade over TMDB’s public API.
> All data returned is subject to TMDB’s Terms of Service; use responsibly.
```

---  

Just drop this content into your `README.md` and you’re all set!
If you’d like a lighter version (no movie helpers) you can still keep the
original example – the new section simply adds an extra usage option.