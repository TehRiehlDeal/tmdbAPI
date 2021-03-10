# tmdbAPI
This is an API library for use when connecting to The TVDB.

## How to Use
```
from tmdbAPI import TMDB

t = TMDB()

# Get basic info about a show
t.getShow("Mythbusters")

# Get a specific episodes name
t.getEpisodeName("Scrubs", 1, 1)
```