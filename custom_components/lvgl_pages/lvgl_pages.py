"""LVGL Pages core function."""

import logging
import sys
import uuid

import yaml

_LOGGER = logging.getLogger(__name__)

try:
    from .const import PageTypes, WidgetTypes
except ImportError:
    _LOGGER.error("Import error from context")
    try:
        from const import PageTypes, WidgetTypes
    except ImportError:
        _LOGGER.error("Import error from local")
        raise


class Widget:
    """Widget class."""

    _config = {}

    def __init__(self, widget_type: WidgetTypes, height, text, icon) -> None:
        """Initialize a widget."""
        self._uid = str(uuid.uuid4())[:8]
        _LOGGER.info(f"Widget UID: {self._uid}")
        self._widget_type = widget_type
        self._height = height
        self._text = text
        self._icon = icon
        self._icon_font = "lv_font_montserrat_24"
        # self._config["UID"] = uuid.uuid4()[:8]

    def add_config(self, config: dict):
        """Add a configuration to the widget."""
        self._config.update(config)

    def get_lvgl(self) -> dict:
        """Return the configuration of the widget."""
        # vars:
        #     uid:
        #     height:
        #     text:
        #     icon:
        #     entity_id:
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


class Page:
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
    #       - lambda: 'lv_indev_wait_release(lv_indev_get_act());'
    #       - logger.log: "Swipe right"
    #       - lvgl.page.next:
    #           animation: OUT_RIGHT
    #           time: 300ms
    #   on_swipe_left:
    #       - lambda: 'lv_indev_wait_release(lv_indev_get_act());'
    #       - logger.log: "Swipe left"
    #       - lvgl.page.previous:
    #           animation: OUT_LEFT
    #           time: 300ms}

    _widgets: list[Widget] = []

    def __init__(self, page_id: str, page_type: PageTypes = PageTypes.Flex) -> None:
        """Initialize a page."""
        self.page_id = page_id
        self.page_type = page_type

    def new_widget(self, **kwargs) -> Widget:
        """Add a widget to the page."""
        widget = Widget(**kwargs)
        self._widgets.append(widget)
        return widget

    def get_lvgl(self, multi_page: bool) -> dict:
        """Return the page as a dictionary."""
        page = {
            "id": self.page_id,
            "width": "100%",
            "bg_color": "black",
            "bg_opa": "cover",
            "pad_all": 5,
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

        if multi_page:
            page.update(
                self._SWIPE_NAVIGATION
            )  # ToDo: Make this a reusable object reference in yaml
        return page

    # def as_dict(self):
    #     """Return the page as a dictionary."""
    #     return {
    #         "id": self.page_id,
    #         "type": self.page_type,
    #         "widgets": [w.as_dict() for w in self.widgets],
    #     }


class LvglPages:
    """LVGL Pages base class."""

    _pages: list[Page] = []

    # def __init__(self) -> None:
    #     """Initialize coordinator."""
    #     pass
    #     # self.page_index = 0

    def new_page(self, page_id: str, **kwargs) -> Page:
        """Add a new page."""
        if not page_id:
            raise ValueError("Page ID is required and be not empty.")
        if len(self._pages) > 0 and [p for p in self._pages if p.page_id == page_id]:
            raise ValueError(f"Page {page_id} already exists.")
        page = Page(page_id, **kwargs)
        self._pages.append(page)
        return page

    def get_lvgl(self) -> str:
        """Return the LVGL Pages as a YAML string."""
        output_data = {"pages": []}
        for page in self._pages:
            output_data["pages"].append(page.get_lvgl(multi_page=len(self._pages) > 1))
        yaml.Dumper.ignore_aliases = lambda *args: True
        return yaml.dump(output_data, allow_unicode=True)

    # def get_lights(self) -> str:
    #     """Return the lights."""
    #     return ""


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    _LOGGER.info("Running test")
    lvgl_pages = LvglPages()
    main_page = lvgl_pages.new_page("main_page")
    r1_widget = main_page.new_widget(
        widget_type=WidgetTypes.Button,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    r2_widget = main_page.new_widget(
        widget_type=WidgetTypes.Button,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    info_page = lvgl_pages.new_page("info_page")
    r3_widget = info_page.new_widget(
        widget_type=WidgetTypes.Button,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    _LOGGER.info(lvgl_pages.get_lvgl())
