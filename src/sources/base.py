"""Base interface for curated data sources."""

from abc import ABC, abstractmethod
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


class Source(ABC):
    """A hand-picked source of investment research data.

    Each source reads from structured YAML files in data/sources/<name>/
    and provides methods to query positions, signals, and diffs.
    """

    @abstractmethod
    def name(self) -> str:
        """Short identifier (e.g. 'leopold', 'baker', 'semianalysis')."""
        ...

    @abstractmethod
    def latest(self) -> dict:
        """Return the most recent data snapshot for this source."""
        ...

    @abstractmethod
    def tickers(self) -> list[str]:
        """Return all tickers this source currently has exposure to."""
        ...

    @abstractmethod
    def lookup(self, ticker: str) -> dict | None:
        """Look up a specific ticker in this source. Returns None if not held."""
        ...
