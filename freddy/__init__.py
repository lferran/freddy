from typing import Any, Dict, Union

from .exceptions import *  # noqa
from .freddy import jsonschema  # noqa
from .freddy import pydantic  # noqa


def sample(_input: Union["pydantic.BaseModel", Dict[str, Any]]) -> Any:
    if isinstance(_input, dict):
        return jsonschema(_input)
    return pydantic(_input)
