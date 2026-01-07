"""Scryfall API client with rate limiting."""

import time
from dataclasses import dataclass

import requests

from transmute.core.exceptions import CardNotFoundError, RateLimitError, ScryfallAPIError
from transmute.core.models import Card


@dataclass
class ScryfallConfig:
    """Configuration for Scryfall API client."""

    base_url: str = "https://api.scryfall.com"
    rate_limit_delay: float = 0.075  # 75ms between requests (Scryfall requirement)
    timeout: float = 10.0
    max_retries: int = 3


class ScryfallClient:
    """Client for Scryfall API with rate limiting and error handling."""

    def __init__(self, config: ScryfallConfig | None = None) -> None:
        self.config = config or ScryfallConfig()
        self._last_request_time: float = 0
        self._session = requests.Session()
        self._session.headers.update(
            {"User-Agent": "Transmute-MTG-Collection-Converter/1.0"}
        )

    def _rate_limit(self) -> None:
        """Ensure we respect Scryfall's rate limit."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.config.rate_limit_delay:
            time.sleep(self.config.rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _request(self, endpoint: str, params: dict[str, str] | None = None) -> dict:
        """Make a rate-limited request to Scryfall."""
        self._rate_limit()

        url = f"{self.config.base_url}{endpoint}"

        try:
            response = self._session.get(url, params=params, timeout=self.config.timeout)
        except requests.RequestException as e:
            raise ScryfallAPIError(f"Request failed: {e}") from e

        data = response.json()

        # Handle errors
        if response.status_code == 404:
            raise CardNotFoundError(data.get("details", "Card not found"))
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        if response.status_code >= 400:
            raise ScryfallAPIError(
                f"API error {response.status_code}: {data.get('details', 'Unknown error')}"
            )

        return data

    def get_card_by_name(
        self,
        name: str,
        set_code: str | None = None,
    ) -> Card:
        """
        Look up a card by name, optionally filtered by set.

        If set_code is provided but no card found, retries without set.
        """
        params = {"exact": name}
        if set_code:
            params["set"] = set_code

        try:
            data = self._request("/cards/named", params)
        except CardNotFoundError:
            if set_code:
                # Retry without set code
                return self.get_card_by_name(name)
            raise

        return self._parse_card_response(data)

    def get_card_by_scryfall_id(self, scryfall_id: str) -> Card:
        """Look up a card by its Scryfall ID."""
        data = self._request(f"/cards/{scryfall_id}")
        return self._parse_card_response(data)

    def _parse_card_response(self, data: dict) -> Card:
        """Convert Scryfall API response to Card model."""
        return Card(
            name=data["name"],
            scryfall_id=data["id"],
            oracle_id=data.get("oracle_id"),
            set_code=data["set"],
            set_name=data["set_name"],
            collector_number=data["collector_number"],
            rarity=data.get("rarity"),
            mana_cost=data.get("mana_cost"),
            type_line=data.get("type_line"),
            colors=data.get("colors"),
            mtgo_id=data.get("mtgo_id"),
            arena_id=data.get("arena_id"),
            tcgplayer_id=data.get("tcgplayer_id"),
            cardmarket_id=data.get("cardmarket_id"),
        )
