"""Common constants for integration."""

from enum import Enum

DOMAIN = "lvgl_pages"


class PageTypes(Enum):
    """Standard numeric identifiers for page types."""

    Flex = 0
    Grid = 1
