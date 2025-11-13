"""Config flow for kosmobot integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import DEFAULT_REGION, DOMAIN


class DkPowerRatesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DK Power Rates."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step of the DK Power Rates config flow."""
        errors = {}
        if user_input is not None:
            # Validate region (should be DK1 or DK2)
            region = user_input["region"].upper()
            if region not in ("DK1", "DK2"):
                errors["region"] = "unknown"
            else:
                await self.async_set_unique_id(region)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"NRGi Power Price {region}", data={"region": region}
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("region", default=DEFAULT_REGION): str}
            ),
            errors=errors,
        )
