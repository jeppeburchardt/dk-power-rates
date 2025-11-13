"""Base entity for DK Power Rates integration."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NrgiCoordinator


class DkPowerEntity(CoordinatorEntity[NrgiCoordinator]):
    """Base entity for DK Power Rates."""

    _attr_has_entity_name = True
