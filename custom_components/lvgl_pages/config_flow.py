"""Config flow for LVGL Pages integration."""

from __future__ import annotations

from copy import deepcopy
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
    callback,
)
from homeassistant.const import CONF_FILE_PATH, CONF_NAME
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LvglPagesConfigFlow(ConfigFlow, domain=DOMAIN):
    """LVGL Pages config flow."""

    VERSION = 0
    MINOR_VERSION = 1
    data = None
    options = None
    _reauth_entry: ConfigEntry | None = None

    async def _validate_file_path(self, file_path: str) -> bool:
        """Ensure the file path is valid."""
        return await self.hass.async_add_executor_job(
            self.hass.config.is_allowed_path, file_path
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle initial user step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._async_abort_entries_match(user_input)
            # await self.async_set_unique_id(self.data[CONF_NAME])
            # self._abort_if_unique_id_configured()

            if not user_input[CONF_NAME]:
                errors[CONF_NAME] = "empty"
            if not await self._validate_file_path(user_input[CONF_FILE_PATH]):
                errors[CONF_FILE_PATH] = "not_allowed"
            else:
                title = f"{user_input[CONF_NAME]} [{user_input[CONF_FILE_PATH]}]"
                self.data = deepcopy(user_input)
                self.options = {}

                _LOGGER.debug(
                    'Creating entry "%s" with data "%s"',
                    self.unique_id,
                    self.data,
                )
                return self.async_create_entry(
                    title=title, data=self.data, options=self.options
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_FILE_PATH): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.TEXT)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            # description_placeholders=placeholders,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> LvglPagesOptionsFlow:
        """Create the options flow."""
        return LvglPagesOptionsFlow(config_entry)


class LvglPagesOptionsFlow(OptionsFlow):
    """Handle File options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage File options."""
        if user_input:
            return self.async_create_entry(data=user_input)

        schema = vol.Schema(
            {
                # vol.Required(CONF_NAME): str,
                vol.Required(CONF_FILE_PATH): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.TEXT)
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                schema, self.config_entry.options or {}
            ),
        )
