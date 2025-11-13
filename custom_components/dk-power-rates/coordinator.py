"""Coordinator for fetching NRGi power price data."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NrgiApiClient, NrgiApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class NrgiCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch and store NRGi power price data."""

    def __init__(
        self, hass: HomeAssistant, client: NrgiApiClient, config_entry: ConfigEntry
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
            config_entry=config_entry,
        )
        self.client = client

    async def _async_update_data(self):
        """Fetch data from the NRGi API for today."""
        now = datetime.now(tz=UTC)
        from_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        to_dt = from_dt + timedelta(days=1) - timedelta(seconds=1)
        try:
            return await self.client.async_get_prices(from_dt, to_dt)
        except NrgiApiError as err:
            raise UpdateFailed(f"Error fetching NRGi data: {err}") from err
