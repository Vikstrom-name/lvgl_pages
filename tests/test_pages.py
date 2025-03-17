"""Pages tests."""

from unittest import mock

from custom_components.lvgl_pages import LvglPages

# from pytest_homeassistant_custom_component.async_mock import patch
# from pytest_homeassistant_custom_component.common import (
#     MockModule,
#     MockPlatform,
#     mock_integration,
#     mock_platform,
# )
from custom_components.lvgl_pages.const import (
    DOMAIN,
)
import pytest

from homeassistant import config_entries
from homeassistant.const import ATTR_NAME, ATTR_UNIT_OF_MEASUREMENT

# from homeassistant.components import sensor
# from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

NAME = "My Pages 1"

CONF_ENTRY = config_entries.ConfigEntry(
    data={
        ATTR_NAME: NAME,
    },
    options={},
    domain=DOMAIN,
    version=2,
    minor_version=0,
    source="user",
    title="LVGL Pages",
    unique_id="123456",
    discovery_keys=None,
)


@pytest.mark.asyncio
async def test_pages_init(hass):
    """Test the pages initialization."""

    # async def async_setup_entry_init(
    #     hass: HomeAssistant, config_entry: config_entries.ConfigEntry
    # ) -> bool:
    #     """Set up test config entry."""
    #     await hass.config_entries.async_forward_entry_setups(
    #         config_entry, [sensor.DOMAIN]
    #     )
    #     return True

    # async def async_setup_entry_platform(
    #     hass: HomeAssistant,
    #     config_entry: config_entries.ConfigEntry,
    #     async_add_entities: AddEntitiesCallback,
    # ) -> None:
    #     """Set up test sensor platform via config entry."""
    #     async_add_entities([np_sensor])

    pages = LvglPages(hass, CONF_ENTRY)

    assert pages.name == NAME
