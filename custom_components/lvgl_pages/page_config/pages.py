"""Individual page properties."""

from abc import ABC
from enum import Enum
import logging

from .widgets import Widget

_LOGGER = logging.getLogger(__name__)


class PageTypes(Enum):
    """Standard numeric identifiers for page types."""

    Flex = 0
    Grid = 1


class Page(ABC):
    """Page class."""

    _SWIPE_NAVIGATION = {
        "on_swipe_right": [
            {"lambda": "lv_indev_wait_release(lv_indev_get_act());"},
            {"logger.log": "Swipe right"},
            {"lvgl.page.next": {"animation": "OUT_RIGHT", "time": "300ms"}},
        ],
        "on_swipe_left": [
            {"lambda": "lv_indev_wait_release(lv_indev_get_act());"},
            {"logger.log": "Swipe left"},
            {"lvgl.page.previous": {"animation": "OUT_LEFT", "time": "300ms"}},
        ],
    }

    _widgets: list[Widget] = []

    def __init__(self, page_id: str, page_type: PageTypes) -> None:
        """Initialize a page."""
        self.page_id = page_id
        self.page_type = page_type

    def new_widget(self, **kwargs) -> Widget:
        """Add a widget to the page."""
        widget = Widget(**kwargs)
        self._widgets.append(widget)
        return widget

    def get_lvgl(self) -> dict:
        """Return the page as a dictionary."""
        page = {
            "id": self.page_id,
            "width": "100%",
            "bg_color": "black",
            "bg_opa": "cover",
            "pad_all": 5,
            **self._SWIPE_NAVIGATION,
            "widgets": [w.get_lvgl() for w in self._widgets],
        }
        if self.page_type == PageTypes.Flex:
            page["layout"] = {
                "type": "flex",
                "flex_flow": "ROW_WRAP",
            }
        elif self.page_type == PageTypes.Grid:
            page["layout"] = {
                "type": "grid",
                "grid_rows": ["fr(1)", "fr(1)"],
                # "grid_columns": ["content", "content", "content", "content", "content", "content", "content"]
                "grid_columns": ["content" for _ in range(7)],
                "pad_column": 4,
                "pad_row": 5,
            }
        else:
            raise ValueError(f"Invalid page type {self.page_type}")

        return page

    def get_assets(self) -> dict:
        """Return the assets for the page."""
        assets = {}
        for widget in self._widgets:
            a = widget.get_assets()
            for key, value in a.items():
                if key in assets:
                    assets[key].extend(value)
                else:
                    assets[key] = value
        return assets
