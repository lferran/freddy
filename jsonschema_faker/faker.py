import copy
import json
import random
import string
from typing import Any, Callable, Dict, List, Optional, Union


"""
# Yet todo
- complete support to basic types (as much as possible)
- support multiple types
- support const
- support definitions/refs
- regular expressions
- support number multipleOf
- support string built-in formats:
  - date-time
  - time
  - date
  - email
  - idn-email
  - hostname
  - idn-hostname
  - ipv4
  - ipv6
  - uri
  - uri-reference
  - iri
  - iri-reference
  - json-pointer
  - relative-json-pointer

# Will not support
- allOf
- not
- conditionals: if, then, else
"""


class UnsupportedType(Exception):
    def __init__(self, _type):
        self._type = _type

    @property
    def type(self):
        return self._type


class UnsupportedSchema(Exception):
    def __init__(self, schema, reason: Optional[str] = None):
        self.schema = schema
        self.reason = reason


class InvalidSchema(Exception):
    def __init__(self, schema, reason: Optional[str] = None):
        self.schema = schema
        self.reason = reason


def _validate_schema(schema: Dict[str, Any], definitions=Optional[Dict[str, Any]]):
    """
    Raise error if schema is not one that we support
    """
    for unsupported in ("allOf", "not", "if", "then", "else", "multipleOf"):
        if unsupported in schema:
            raise UnsupportedSchema(
                schema, reason=f"{unsupported} key is not supported"
            )

    # Check that reference is present
    ref = schema.get("$ref")
    if ref:
        refname = ref.lstrip("#/definitions/")
        if not definitions:
            raise InvalidSchema(schema, reason=f"{refname} not present in definitions")

        if refname not in definitions:
            raise InvalidSchema(schema, reason=f"{refname} not present in definitions")

    _type = schema.get("type")
    enum = schema.get("enum")
    if not _type and not enum and not ref:
        raise UnsupportedSchema(schema, reason=f"type key is required")


def generate(
    schema: Dict[str, Any], _definitions: Optional[Dict[str, Any]] = None
) -> Any:
    # Save copy of input schema if it's first time
    if _definitions is None:
        try:
            _definitions = copy.deepcopy(schema["definitions"])
        except KeyError:
            _definitions = None

    _validate_schema(schema, _definitions)

    for key in ("anyOf", "oneOf"):
        if key in schema:
            return generate_of(schema[key], _definitions)

    if "enum" in schema:
        return generate_enum(schema["enum"])

    if "$ref" in schema:
        refname = schema["$ref"].lstrip("#/definitions/")
        refschema = _definitions[refname]  # type: ignore
        handler = get_definition_generator(refschema)
        return handler(_definitions)

    handlers = {
        "null": lambda s: None,
        "boolean": generate_boolean,
        "string": generate_string,
        "integer": generate_integer,
        "number": generate_number,
        "array": generate_array,
        "object": generate_object,
    }

    _type = schema["type"]
    try:
        handler = handlers[_type]  # type: ignore
    except KeyError:
        raise UnsupportedType(_type)

    if _type in ("array", "object"):
        return handler(schema, _definitions)
    else:
        # Basic type
        return handler(schema)


def generate_string(schema: Dict[str, Any]) -> str:
    minlength = schema.get("minLength", 0)
    maxlength = schema.get("maxLength", 10)
    length = random.randint(minlength, maxlength)
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_integer(schema: Dict[str, Any]) -> int:
    # Try getting minimum and maximum
    minimum = schema.get("minimum", 0)
    maximum = schema.get("maximum", 100)
    # Support exclusives
    try:
        if schema["exclusiveMinimum"]:
            minimum += 1
    except KeyError:
        pass
    try:
        if schema["exclusiveMaximum"]:
            maximum -= 1
    except KeyError:
        pass
    return random.randint(minimum, maximum)


def generate_number(schema: Dict[str, Any]) -> Union[int, float]:
    minimum = schema.get("minimum", 0)
    maximum = schema.get("maximum", 100)
    if random.randint(0, 1):
        return random.randint(minimum, maximum)
    return random.uniform(minimum, maximum)


def generate_enum(choices: List[Any]) -> Any:
    return random.choice(choices)


def generate_array(
    schema: Dict[str, Any], definitions: Optional[Dict[str, Any]] = None
) -> List[Any]:
    maxitems = schema.get("maxItems", 10)
    minitems = schema.get("minItems", 0)
    items_schema = schema["items"]
    return [
        generate(items_schema, _definitions=definitions)
        for i in range(random.randint(minitems, maxitems))
    ]


def generate_object(
    schema: Dict[str, Any], definitions: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        key: generate(key_schema, _definitions=definitions)
        for key, key_schema in schema.get("properties", {}).items()
    }


def generate_boolean(schema: Dict[str, Any]) -> bool:
    return random.choice([True, False])


def generate_of(
    schemas: List[Dict[str, Any]], definitions: Optional[Dict[str, Any]] = None
) -> Any:
    return generate(random.choice(schemas), _definitions=definitions)


def get_definition_generator(schema: Dict[str, Any]) -> Callable:
    def new_func(definitions: Optional[Dict[str, Any]] = None):
        return generate(schema, _definitions=definitions)

    return new_func
