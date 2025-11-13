"""Sensor platform for kosmobot NRGi power price."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NrgiCoordinator
from .entity import DkPowerEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up kosmobot sensor from config entry."""
    coordinator: NrgiCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DkPowerCurrentRateSensor(coordinator)])


class DkPowerCurrentRateSensor(DkPowerEntity, SensorEntity):
    """Sensor to represent the current NRGi power price."""

    _attr_translation_key = "current_rate"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "kr/kWh"

    def __init__(self, coordinator: NrgiCoordinator) -> None:
        super().__init__(coordinator)
        entry = getattr(coordinator, "config_entry", None)
        region = None
        if entry is not None:
            region = entry.data.get("region", "DK2")
            self._attr_unique_id = f"{entry.entry_id}_current_rate"
        else:
            self._attr_unique_id = None
        # Set a human-friendly name
        self._attr_name = (
            f"DK Power Current Rate ({region})" if region else "DK Power Current Rate"
        )

    @property
    def native_value(self) -> float | None:
        """Return the current kr/kWh rate."""
        data = self.coordinator.data
        if not data or "currentPrice" not in data:
            return None
        price = data.get("currentPrice")
        if price is not None:
            return round(price / 100, 2)
        return None
