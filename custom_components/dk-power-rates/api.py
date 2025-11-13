"""API client for NRGi power price data."""

from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

import aiohttp

from .const import API_URL_NRGI

_LOGGER = logging.getLogger(__name__)


class NrgiApiClient:
    """Client to interact with the NRGi API."""

    def __init__(self, session: aiohttp.ClientSession, region: str) -> None:
        self._session = session
        self._region = region

    async def async_get_prices(
        self, from_dt: datetime, to_dt: datetime
    ) -> dict[str, Any]:
        """Fetches latest rates from Nrgi API."""
        params = {
            "region": self._region,
            "from": from_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "to": to_dt.strftime("%Y-%m-%dT%H:%M:%S.999Z"),
            "includeGrid": "true",
            "resolution": "PT1H",
        }
        url = API_URL_NRGI
        _LOGGER.debug("Requesting NRGi API: %s params=%s", url, params)
        try:
            async with self._session.get(url, params=params) as resp:
                resp.raise_for_status()
                data = await resp.json()
                _LOGGER.debug(
                    "NRGi API success: %s params=%s response=%s", url, params, data
                )
                return data
        except Exception as err:
            _LOGGER.debug(
                "NRGi API request failed: %s params=%s error=%s", url, params, err
            )
            raise NrgiApiError(f"NRGi API request failed: {err}") from err


class NrgiApiError(Exception):
    """Exception raised for errors in the NRGi API client."""
