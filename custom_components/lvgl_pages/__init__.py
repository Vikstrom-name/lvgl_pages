"""Main package for LVGL pages."""

from __future__ import annotations

import logging
import os
import pathlib

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_ID, CONF_FILE_PATH, CONF_PLATFORM, Platform
from homeassistant.core import HomeAssistant, HomeAssistantError
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .config_flow import LvglPagesConfigFlow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    filepath: str = config_entry.data[CONF_FILE_PATH]
    if not await hass.async_add_executor_job(hass.config.is_allowed_path, filepath):
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="dir_not_allowed",
            translation_placeholders={"filename": filepath},
        )

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if config_entry.entry_id not in hass.data[DOMAIN]:
        pages = LvglPagesCoordinator(hass, config_entry)
        # await pages.async_setup()
        hass.data[DOMAIN][config_entry.entry_id] = pages

    # await hass.config_entries.async_forward_entry_setups(
    #     config_entry, [Platform(config_entry.data[CONF_PLATFORM])]
    # )

    hass.services.async_register(
        DOMAIN,
        service="write_config",
        service_func=pages.write_config,
        schema=vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): cv.string,
                vol.Required("page_name"): cv.string,
                vol.Optional("widget_1"): cv.string,
            },
            required=True,
        ),
    )

    config_entry.async_on_unload(config_entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # return await hass.config_entries.async_unload_platforms(
    #     entry, [entry.data[CONF_PLATFORM]]
    # )
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


# async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
#     """Migrate old entry."""
#     _LOGGER.debug(
#         "Attempting migrating configuration from version %s.%s",
#         config_entry.version,
#         config_entry.minor_version,
#     )

#     class MigrateError(HomeAssistantError):
#         """Error to indicate there is was an error in version migration."""

#     installed_version = LvglPagesConfigFlow.VERSION
#     installed_minor_version = LvglPagesConfigFlow.MINOR_VERSION

#     new_data = {**config_entry.data}
#     new_options = {**config_entry.options}

#     if config_entry.version > installed_version:
#         _LOGGER.warning(
#             "Downgrading major version from %s to %s is not allowed",
#             config_entry.version,
#             installed_version,
#         )
#         return False

#     if (
#         config_entry.version == installed_version
#         and config_entry.minor_version > installed_minor_version
#     ):
#         _LOGGER.warning(
#             "Downgrading minor version from %s.%s to %s.%s is not allowed",
#             config_entry.version,
#             config_entry.minor_version,
#             installed_version,
#             installed_minor_version,
#         )
#         return False

#     hass.config_entries.async_update_entry(
#         config_entry,
#         data=new_data,
#         options=new_options,
#         version=installed_version,
#         minor_version=installed_minor_version,
#     )
#     _LOGGER.info(
#         "Migration configuration from version %s.%s to %s.%s successful",
#         config_entry.version,
#         config_entry.minor_version,
#         installed_version,
#         installed_minor_version,
#     )
#     return True


class LvglPagesCoordinator:
    """LVGL Pages coordinator class."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize my coordinator."""
        self._hass = hass
        self._config = config_entry
        self._state_change_listeners = []

    def as_dict(self):
        """For diagnostics serialization."""
        res = self.__dict__.copy()
        # for k, i in res.copy().items():
        #     if "_number_entity" in k:
        #         res[k] = {"id": i, "value": self.get_number_entity_value(i)}
        return res

    @property
    def name(self) -> str:
        """Name of pages."""
        return self._config.data["name"]

    def get_device_info(self) -> DeviceInfo:
        """Get device info to group entities."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config.entry_id)},
            name=self.name,
            manufacturer="LVGL",
            entry_type=DeviceEntryType.SERVICE,
            # model="Forecast",
        )

    def update(self):
        """Update the pages."""
        _LOGGER.debug("Updating pages")

    def export_config(self):
        """Export the configuration."""
        _LOGGER.debug("Exporting configuration")

    async def write_config(self, call):
        """Execute a service with an action command to Easee charging station."""
        _LOGGER.debug("Call write config %s", call.data)

        export_path = pathlib.Path(self._config.data[CONF_FILE_PATH]).joinpath(
            self._config.data["name"]
        )

        try:
            export_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise HomeAssistantError("Could not create config path") from e

        try:
            with open(export_path.joinpath("lvgl.yaml"), "w", encoding="utf8") as f:
                f.write("Hello, World!")
            with open(export_path.joinpath("assets.yaml"), "w", encoding="utf8") as f:
                f.write("Hello, World!")
        except OSError as e:
            raise HomeAssistantError("Could not write config") from e

        return True
