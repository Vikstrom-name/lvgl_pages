"""Page collection package."""

import yaml

from .pages import Page, PageTypes
from .widgets import Widget, WidgetTypes


def dict_to_yaml_str(config: dict) -> str:
    """Convert a dictionary to a YAML string."""
    yaml.Dumper.ignore_aliases = lambda *args: True
    return yaml.dump(config, allow_unicode=True)
