from typing import Any

from .exceptions import *  # noqa
from .freddy import jsonschema  # noqa
from .freddy import pydantic  # noqa


def sample(_input) -> Any:
    if isinstance(_input, dict):
        return jsonschema(_input)
    return pydantic(_input)
