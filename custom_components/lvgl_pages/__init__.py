"""Main package for LVGL pages."""

from __future__ import annotations

import datetime as dt
import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    Platform,
)
from homeassistant.core import HomeAssistant, HomeAssistantError
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)
from homeassistant.util import dt as dt_util

from .config_flow import LvglPagesConfigFlow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if config_entry.entry_id not in hass.data[DOMAIN]:
        pages = LvglPages(hass, config_entry)
        await pages.async_setup()
        hass.data[DOMAIN][config_entry.entry_id] = pages

    if config_entry is not None:
        if config_entry.source == SOURCE_IMPORT:
            hass.async_create_task(
                hass.config_entries.async_remove(config_entry.entry_id)
            )
            return False

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unloading a config_flow entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        pages = hass.data[DOMAIN].pop(entry.entry_id)
        pages.cleanup()
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload the config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug(
        "Attempting migrating configuration from version %s.%s",
        config_entry.version,
        config_entry.minor_version,
    )

    class MigrateError(HomeAssistantError):
        """Error to indicate there is was an error in version migration."""

    installed_version = LvglPagesConfigFlow.VERSION
    installed_minor_version = LvglPagesConfigFlow.MINOR_VERSION

    new_data = {**config_entry.data}
    new_options = {**config_entry.options}

    if config_entry.version > installed_version:
        _LOGGER.warning(
            "Downgrading major version from %s to %s is not allowed",
            config_entry.version,
            installed_version,
        )
        return False

    if (
        config_entry.version == installed_version
        and config_entry.minor_version > installed_minor_version
    ):
        _LOGGER.warning(
            "Downgrading minor version from %s.%s to %s.%s is not allowed",
            config_entry.version,
            config_entry.minor_version,
            installed_version,
            installed_minor_version,
        )
        return False

    hass.config_entries.async_update_entry(
        config_entry,
        data=new_data,
        options=new_options,
        version=installed_version,
        minor_version=installed_minor_version,
    )
    _LOGGER.info(
        "Migration configuration from version %s.%s to %s.%s successful",
        config_entry.version,
        config_entry.minor_version,
        installed_version,
        installed_minor_version,
    )
    return True


class LvglPages:
    """LVGL Pages base class."""

    _hourly_update = None

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

    async def async_setup(self):
        """Post initialization setup."""
        # Ensure an update is done on every hour
        # self._hourly_update = async_track_time_change(
        #     self._hass, self.scheduled_update, minute=0, second=0
        # )

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

    def scheduled_update(self, _):
        """Scheduled updates callback."""
        _LOGGER.debug("Scheduled callback")
        self.update()

    def update(self):
        """Update the pages."""
        _LOGGER.debug("Updating pages")
