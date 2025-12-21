# settings.py
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

# Optionally use python‑dotenv so that the .env file is read automatically
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dot-env is optional – the env may already be set by CI

@dataclass(frozen=True)
class Settings:
    api_key: Optional[str] = os.getenv("TMDB_API_KEY")
    base_url: str = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
    timeout: float = 10.0

# Export a single instance so that the rest of the code can import it
settings = Settings()