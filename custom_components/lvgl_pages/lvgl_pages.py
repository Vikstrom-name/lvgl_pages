"""LVGL Pages core function."""

from .const import PageTypes


class Widget:
    """Widget class."""

    def __init__(self, widget_type: str):
        """Initialize a widget."""
        self.widget_type = widget_type
        self.config = {}

    def add_config(self, config: dict):
        """Add a configuration to the widget."""
        self.config.update(config)

    # def as_dict(self):
    #     """Return the widget as a dictionary."""
    #     return {
    #         "type": self.widget_type,
    #         "config": self.config,
    #     }


class Page:
    """Page class."""

    def __init__(self, page_id: str, page_type: PageTypes = PageTypes.Flex):
        """Initialize a page."""
        self.page_id = page_id
        self.page_type = page_type
        self.widgets = []

    def new_widget(self) -> Widget:
        """Add a widget to the page."""
        widget = Widget()
        self.widgets.append(widget)
        return widget

    # def as_dict(self):
    #     """Return the page as a dictionary."""
    #     return {
    #         "id": self.page_id,
    #         "type": self.page_type,
    #         "widgets": [w.as_dict() for w in self.widgets],
    #     }


class LvglPages:
    """LVGL Pages base class."""

    pages = {}

    def __init__(self):
        """Initialize coordinator."""
        pass
        # self.page_index = 0

    def new_page(self, page_id: str, page_type: PageTypes = PageTypes.Flex) -> Page:
        """Add a new page."""
        if page_id in self.pages:
            raise ValueError(f"Page {page_id} already exists.")
        page = Page(page_id, page_type)
        self.pages[page_id] = page
        return page

    # async def async_setup(self):
    #     """Set up the LVGL Pages."""
    #     self.hass.http.register_static_path('/lvgl_pages', self.hass.config.path


""" Example of page configuration
lvgl:
  pages:
    - id: main_page
      layout:
        type: flex
        flex_flow: ROW_WRAP
      width: 100%
      bg_color: black
      bg_opa: cover
      pad_all: 5
      <<: !include {file: agillis-lvgl/modules/sections/swipe_navigation.yaml}
      widgets:
        # - label:
        #     align: CENTER
        #     text: 'Hello World!'
        - button: !include
            file: agillis-lvgl/modules/buttons/local_relay_button.yaml
            vars:
              uid: button_1
              height: $button_height_double
              text: Light 1
              icon: $lightbulb
        - button: !include
            file: agillis-lvgl/modules/buttons/local_relay_button.yaml
            vars:
              uid: button_2
              height: $button_height_double
              text: Light 2
              icon: $lightbulb
        - button: !include
            file: agillis-lvgl/modules/buttons/local_relay_button.yaml
            vars:
              uid: button_3
              height: $button_height_double
              text: Light 3
              icon: $lightbulb
"""
