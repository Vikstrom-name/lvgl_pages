"""LVGL Pages core function."""

import logging
import sys

import custom_components.lvgl_pages.page_config as page_config

_LOGGER = logging.getLogger(__name__)


class LvglPages:
    """LVGL Pages base class."""

    _pages: list[page_config.Page] = []

    # def __init__(self) -> None:
    #     """Initialize page coordinator."""

    def new_page(self, page_id: str, **kwargs) -> page_config.Page:
        """Add a new page."""
        if not page_id:
            raise ValueError("Page ID is required and not empty.")
        if [p for p in self._pages if p.page_id == page_id]:
            raise ValueError(f"Page {page_id} already exists.")
        page = page_config.Page(page_id, **kwargs)
        self._pages.append(page)
        return page

    def get_all_lvgl(self) -> str:
        """Return the LVGL Pages as a YAML string."""
        output_data = {"pages": []}
        for page in self._pages:
            output_data["pages"].append(page.get_lvgl())
        return page_config.dict_to_yaml_str(output_data)

    def get_all_assets(self) -> str:
        """Return the assets."""
        output_data = {}
        for page in self._pages:
            a = page.get_assets()
            for key, value in a.items():
                if key in output_data:
                    output_data[key].extend(value)
                else:
                    output_data[key] = value
            # output_data.update(page.get_assets())
        return page_config.dict_to_yaml_str(output_data)


if __name__ == "__main__":
    # To run from command line, mostly for testing during development.
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    _LOGGER.info("Running test")
    main_page = page_config.Page("main_page", page_type=page_config.PageTypes.Flex)
    ll_1_widget = main_page.new_widget(
        widget_type=page_config.WidgetTypes.LocalLightButton,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    ll_2_widget = main_page.new_widget(
        widget_type=page_config.WidgetTypes.LocalLightButton,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    rl_1_widget = main_page.new_widget(
        widget_type=page_config.WidgetTypes.RemoteLightButton,
        height=50,
        text="Toggle",
        icon="mdi:lightbulb",
    )
    lvgl = main_page.get_lvgl()
    assets = main_page.get_assets()
    _LOGGER.info("### The pages ###")
    _LOGGER.info(lvgl)
    _LOGGER.info("### The assets ###")
    _LOGGER.info(assets)

    # _LOGGER.info("Running test")
    # lvgl_pages = LvglPages()
    # main_page = lvgl_pages.new_page("main_page", page_type=page_config.PageTypes.Flex)
    # r1_widget = main_page.new_widget(
    #     widget_type=page_config.WidgetTypes.LightButton,
    #     height=50,
    #     text="Toggle",
    #     icon="mdi:lightbulb",
    # )
    # r2_widget = main_page.new_widget(
    #     widget_type=page_config.WidgetTypes.LightButton,
    #     height=50,
    #     text="Toggle",
    #     icon="mdi:lightbulb",
    # )
    # info_page = lvgl_pages.new_page("info_page", page_type=page_config.PageTypes.Flex)
    # r3_widget = info_page.new_widget(
    #     widget_type=page_config.WidgetTypes.LightButton,
    #     height=50,
    #     text="Toggle",
    #     icon="mdi:lightbulb",
    # )
    # _LOGGER.info("### The pages ###")
    # _LOGGER.info(lvgl_pages.get_all_lvgl())
    # _LOGGER.info("### The assets ###")
    # _LOGGER.info(lvgl_pages.get_all_assets())
