"""13F fund source — reads quarterly YAML filings for Leopold and Baker."""

from pathlib import Path

import yaml

from src.sources.base import DATA_DIR, Source


class Fund13FSource(Source):
    """Reads 13F position data from data/sources/<fund_name>/."""

    def __init__(self, fund_name: str):
        self._name = fund_name
        self._dir = DATA_DIR / "sources" / fund_name
        self._data: dict | None = None

    def name(self) -> str:
        return self._name

    def _load_latest(self) -> dict:
        """Find and load the most recent quarterly YAML file."""
        if self._data is not None:
            return self._data

        files = sorted(self._dir.glob("q*.yaml"), reverse=True)
        if not files:
            return {}

        with open(files[0]) as f:
            self._data = yaml.safe_load(f)
        return self._data

    def latest(self) -> dict:
        return self._load_latest()

    def all_quarters(self) -> list[dict]:
        """Load all quarterly filings, newest first."""
        results = []
        for f in sorted(self._dir.glob("q*.yaml"), reverse=True):
            with open(f) as fh:
                results.append(yaml.safe_load(fh))
        return results

    def tickers(self) -> list[str]:
        data = self._load_latest()
        return [p["ticker"] for p in data.get("positions", [])]

    def lookup(self, ticker: str) -> dict | None:
        data = self._load_latest()
        for p in data.get("positions", []):
            if p["ticker"] == ticker:
                return p
        return None

    def exits(self) -> list[dict]:
        """Return positions exited in the most recent quarter."""
        data = self._load_latest()
        return data.get("exits", [])

    def by_bottleneck(self, bottleneck: str) -> list[dict]:
        """Return all positions mapped to a specific bottleneck."""
        data = self._load_latest()
        return [p for p in data.get("positions", []) if p.get("bottleneck") == bottleneck]

    def summary(self) -> dict:
        """Return fund-level metadata."""
        data = self._load_latest()
        return {
            "entity": data.get("entity"),
            "quarter": data.get("quarter"),
            "filed": data.get("filed"),
            "aum": data.get("aum"),
            "positions_count": data.get("positions_count"),
            "top5_concentration": data.get("top5_concentration"),
        }
