"""Config flow for LVGL Pages integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import ATTR_NAME, ATTR_UNIT_OF_MEASUREMENT
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector, template

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LvglPagesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """LVGL Pages config flow."""

    VERSION = 0
    MINOR_VERSION = 1
    data = None
    options = None
    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle initial user step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self.data = user_input
            # Add those that are not optional

            self.options = {}

            await self.async_set_unique_id(self.data[ATTR_NAME])
            self._abort_if_unique_id_configured()

            _LOGGER.debug(
                'Creating entry "%s" with data "%s"',
                self.unique_id,
                self.data,
            )
            return self.async_create_entry(
                title=self.data[ATTR_NAME], data=self.data, options=self.options
            )

        schema = vol.Schema(
            {
                vol.Required(ATTR_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            # description_placeholders=placeholders,
            errors=errors,
        )
