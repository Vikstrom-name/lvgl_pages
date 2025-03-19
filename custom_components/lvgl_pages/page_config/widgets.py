"""Individual widgets properties."""

from abc import ABC
from enum import Enum
import logging
import uuid

_LOGGER = logging.getLogger(__name__)


class WidgetTypes(Enum):
    """Standard numeric identifiers for widget types."""

    LocalLightButton = 1
    RemoteLightButton = 2


class Widget(ABC):
    """Widget class."""

    _config = {}

    def __init__(self, widget_type: WidgetTypes, height, text, icon) -> None:
        """Initialize a widget."""
        self._uid = str(uuid.uuid4())[:8]
        # _LOGGER.info(f"Widget UID: {self._uid}")
        self._widget_type = widget_type
        self._height = height
        self._text = text
        self._icon = icon
        self._icon_font = "lv_font_montserrat_24"

    def add_config(self, config: dict):
        """Add a configuration to the widget."""
        self._config.update(config)

    def get_lvgl(self) -> dict:
        """Return the configuration of the widget."""
        widget = {
            "height": self._height,
            "id": f"button_{self._uid}",
            "widgets": [
                {
                    "label": {
                        "text_font": self._icon_font,
                        "align": "top_left",
                        "id": f"icon_{self._uid}",
                        "text": self._icon,
                    }
                },
                {
                    "label": {
                        "align": "bottom_left",
                        "id": f"label_{self._uid}",
                        "text": self._text,
                    }
                },
            ],
            "on_short_click": {"light.toggle": f"local_light_{self._uid}"},
        }
        return widget
        # height: ${height}
        # id: button_${uid}
        # widgets:
        # - label:
        #     text_font: $icon_font
        #     align: top_left
        #     id: icon_${uid}
        #     text: ${icon}
        # - label:
        #     align: bottom_left
        #     id: label_${uid}
        #     text: ${text}
        # on_short_click:
        #     light.toggle: local_light_${uid}

    def get_assets(self) -> dict:
        """Return the assets for the widget."""
        assets = {
            "light": [
                {
                    "id": f"local_light_{self._uid}",
                    "name": self._text,
                    "platform": "binary",
                    "output": f"local_light_{self._uid}",
                    "on_turn_on": {
                        "then": [
                            {
                                "lvgl.widget.update": {
                                    "id": f"button_{self._uid}",
                                    "bg_color": "$button_on_color",
                                }
                            },
                            {
                                "lvgl.widget.update": {
                                    "id": f"icon_{self._uid}",
                                    "text_color": "$icon_on_color",
                                }
                            },
                            {
                                "lvgl.widget.update": {
                                    "id": f"label_{self._uid}",
                                    "text_color": "$label_on_color",
                                }
                            },
                        ]
                    },
                    "on_turn_off": {
                        "then": [
                            {
                                "lvgl.widget.update": {
                                    "id": f"button_{self._uid}",
                                    "bg_color": "$button_off_color",
                                }
                            },
                            {
                                "lvgl.widget.update": {
                                    "id": f"icon_{self._uid}",
                                    "text_color": "$icon_off_color",
                                }
                            },
                            {
                                "lvgl.widget.update": {
                                    "id": f"label_{self._uid}",
                                    "text_color": "$label_off_color",
                                }
                            },
                        ]
                    },
                }
            ]
        }
        # light:
        #   - id: local_light_${uid}
        #     name: ${ha_name}
        #     platform: binary
        #     output: $entity_id
        #     on_turn_on:
        #       then:
        #         - lvgl.widget.update:
        #             id: button_${uid}
        #             bg_color: $button_on_color
        #         - lvgl.widget.update:
        #             id: icon_${uid}
        #             text_color: $icon_on_color
        #         - lvgl.widget.update:
        #             id: label_${uid}
        #             text_color: $label_on_color
        #     on_turn_off:
        #       then:
        #         - lvgl.widget.update:
        #             id: button_${uid}
        #             bg_color: $button_off_color
        #         - lvgl.widget.update:
        #             id: icon_${uid}
        #             text_color: $icon_off_color
        #         - lvgl.widget.update:
        #             id: label_${uid}
        #             text_color: $label_off_color
        return assets
